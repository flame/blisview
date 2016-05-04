# BLIS Performance graphs project
# The University of Texas at Austin
# Author(s): Barrett Hinson

from django.contrib import admin

from .models import Attribute, Options, Graph, Ent_Assoc

admin.site.register(Attribute)
admin.site.register(Options)
admin.site.register(Graph)
admin.site.register(Ent_Assoc)