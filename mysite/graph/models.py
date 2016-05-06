# BLIS Performance graphs project
# The University of Texas at Austin
# Author(s): Barrett Hinson

from django.db import models

# the model for the various attrubutes a user can choose from (ie: Datatype, Operation)
class Attribute(models.Model):
    attribute_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.attribute_text

# the model for the various options within an attrubutes a user can choose from (ie: syrk, gemm)
class Options(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    options_text = models.CharField(max_length=200)
    test_input = models.CharField(default='0', max_length=200)
    def __str__(self):
        return self.options_text

# the model for storing the location of a graph image, name is determined via primary key
class Graph(models.Model):
    path_static = models.FilePathField(path="", allow_files=True)
    path_template = models.FilePathField(path="", allow_files=True)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

# associates graph objects to option objects for thier many to many relationship
class Ent_Assoc(models.Model):
    option = models.ForeignKey(Options, on_delete=models.CASCADE)
    graph = models.ForeignKey(Graph, on_delete=models.CASCADE)
    def __str__(self):
        return "Entity Association: " + self.option.options_text + " & " + self.graph.name


