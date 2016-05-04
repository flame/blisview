# BLIS Performance graphs project
# The University of Texas at Austin
# Author(s): Barrett Hinson

from django.db import models

class Attribute(models.Model):
    attribute_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.attribute_text


class Options(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    options_text = models.CharField(max_length=200)
    test_input = models.CharField(default='0', max_length=200)
    def __str__(self):
        return self.options_text
    #can add normal python methods here as needed
    #idea 1: method to rerun the tests when a new option is chosen
    #idea 2: the votes property can be used to keep track of the most
    #         often used settings and base the defaults off of that

class Graph(models.Model):
    path_static = models.FilePathField(path="", allow_files=True)
    path_template = models.FilePathField(path="", allow_files=True)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    # def generate(self, selected_options):


class Ent_Assoc(models.Model):
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    def __str__(self):
        return "Entity Association: " + self.option.options_text + " & " + self.graph.name


