# BLIS Performance graphs project
# The University of Texas at Austin
# Author(s): Barrett Hinson

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.staticfiles.templatetags.staticfiles import static
from .models import Attribute, Options, Graph, Ent_Assoc
from subprocess import call
import matplotlib.pyplot as plt
import numpy as np


# ----------------------------------------------------------------------
# SET YOUR BLIS TEST-SUITE BUILD LOCATION
Test_Suite = 'graph/static/graph/blis/testsuite/'
#-----------------------------------------------------------------------




# home webpage view, /graph/ 
def index(request):
    attribute_list = Attribute.objects.order_by('-pub_date')[:]
    context = {
        'attribute_list': attribute_list,
    }
    return render(request, 'graph/index.html', context)

# this view is a reposotory of all our currently generated graphs
def repo(request):
    attribute_list = Attribute.objects.order_by('-pub_date')[:5]
    graph_list = Graph.objects.all()
    context = {
        'attribute_list': attribute_list,
        'graph_list':graph_list,
    }
    return render(request, 'graph/repo.html', context)

#this view is called when a user submits a specific set of parameters
def submit(request):
    # force_redo should be added as an admin option, or maybe even a user faceing option,
    # it forces the rerun of the tests and redraw of the graphs, while not chaging
    # the database entries
    force_redo = 0;

    # this code checks the databases to see if our graph if already present or not
    # it does this by filtering through the entity association table, and
    # seeing if the expexted entries are present, if not, time to make a new graph
    attribute_list = Attribute.objects.order_by('-pub_date')[:]
    graph_list = Graph.objects.all()
    selected_options = {}
    for attribute in attribute_list:
        selected_options[attribute.attribute_text] = request.POST[attribute.attribute_text]
        print(attribute.attribute_text+": "+selected_options[attribute.attribute_text])

    primary_key = 0

    or_set = Ent_Assoc.objects.filter(pk = None)
    for option_val in selected_options.values():
        or_set = or_set.__or__(Ent_Assoc.objects.filter(option = option_val))

    filter_set = {}
    for entity in or_set:
        entity_name = entity.graph.name
        if(filter_set.keys().__contains__(entity_name)):
            filter_set[entity_name] += 1
            if(filter_set[entity_name] == len(selected_options)):
                primary_key = entity.graph.pk
        else:
            filter_set[entity_name] = 1
    
    # this variable prevents the rerunning of the tests when force_redo is checked but it is the first time running it
    first_created = 0

    #this means the graph is not already present, so we need to make it
    if(primary_key == 0):
        # the block ceates the Graph object an inserts it to the Graph database
        next_ind = 0
        name_gen = ""
        for attribute in attribute_list:
            name_gen += attribute.attribute_text+": "+Options.objects.get(pk=selected_options[attribute.attribute_text]).options_text+", "
        g = Graph(path_static = "images/$.png", path_template = "graph/images/$.png", name = name_gen)
        g.save()
        next_ind = g.pk
        print("\n next ind: "+str(next_ind)+" and pk: "+str(g.pk))
        g.path_static = "images/"+str(next_ind)+".png"
        g.path_template = "graph/images/"+str(next_ind)+".png"
        g.save()
        print("\n next ind: "+str(next_ind)+" and pk: "+str(g.pk))

        # the block generates all of the entity associations between the graph and the options
        for attribute in attribute_list:
            e = Ent_Assoc(option = Options.objects.get(pk=selected_options[attribute.attribute_text]), graph = Graph.objects.get(pk=g.pk))
            e.save()

        # this block creates the test suite input files, and runs the tests, and plots the results
        primary_key = next_ind
        create_test_files(selected_options)
        run_performance_tests(primary_key, Options.objects.get(pk=selected_options["Operation"]).options_text)
        create_graph(primary_key)

        first_created = 1

    if(force_redo == 1 and first_created == 0):
        create_test_files(selected_options)
        run_performance_tests(primary_key, Options.objects.get(pk=selected_options["Operation"]).options_text)
        create_graph(primary_key)
        

    return HttpResponseRedirect(reverse('graph:results', args=(primary_key,)))

# this view shows the resultent graph after a user selects custom options
def results(request, graph_id):
    graph_result = get_object_or_404(Graph, pk=graph_id)
    return render(request, 'graph/results.html', {'graph_result': graph_result})

# this view shows a simple about page, nothing big
def about(request):
    return render(request, 'graph/about.html', {})

#this method could use ALOT of cleaning up, sorry
# this generates the test suite input files via using a template file and finding/replacing placeholders in it (denoted via '$')
def create_test_files(selected_options):
    input_general = open('graph/static/graph/template_input.general', "r")
    new_input = open(Test_Suite + 'input.general',"w")  
    for line in input_general:
        nline = line
        for attribute in selected_options.keys():
            if ("$"+attribute) in line:
                nline = line.replace("$"+attribute, Options.objects.get(pk=selected_options[attribute]).test_input)
        new_input.write(nline)
    input_general.close()
    new_input.close()
    
    input_operations = open('graph/static/graph/template_input.operations', "r")
    new_operations = open(Test_Suite + 'input.operations', "w")
    for line in input_operations:
        nline = line
        if ("$Operation") in line:
            if selected_options['Operation'] in line:
                nline = nline.replace("$Operation"+selected_options['Operation'], '1')
            else:
                nline = nline.replace("$Operation14", '0')
                nline = nline.replace("$Operation15", '0')
                nline = nline.replace("$Operation16", '0')
        new_operations.write(nline)
    input_operations.close()
    new_operations.close()

# this method runs the test suite with our generated test input files 
def run_performance_tests(name, operation):
    call([Test_Suite + "test_libblis.x", "-g", Test_Suite + "input.general", "-o", Test_Suite + "input.operations" ])
    call(["mv", "libblis_test_"+operation+".m", Test_Suite+str(name)+".m"])

# this method does all of the Matpotlib graphing/plotting of the test results
def create_graph(name):
    results_file = open(Test_Suite+str(name)+".m", "r")
    x = [0]
    y = [0]
    peak = [59.2]
    for line in results_file:
        if "%" not in line:
            lineP = line.split()
            if len(lineP) > 0 and "blis" in lineP[0]:
                x.append(float(lineP[1]))
                y.append(float(lineP[len(lineP)-3]))
                peak.append(59.2)
    performance, = plt.plot(x, y, "g-", linewidth=2.0, label = "Performance")
    peak, = plt.plot(x, peak, "r--", linewidth=2.0, label = "Theoretical Peak")
    plt.xlabel("Problem Size (m = n = k)")
    plt.ylabel("GFLOPS")
    plt.grid()
    plt.legend(loc=4)
    plt.savefig(str(name)+".png", dpi=70)
    plt.close()
    results_file.close()
    call(["mv", str(name)+".png", "graph/static/graph/images/"+str(name)+".png"])
