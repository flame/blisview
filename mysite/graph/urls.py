# BLIS Performance graphs project
# The University of Texas at Austin
# Author(s): Barrett Hinson

from django.conf.urls import url

from . import views

app_name = 'graph'
urlpatterns = [
	# ie: /graph/
    url(r'^$', views.index, name='index'),
    #ie: /graph/repo/
    url(r'^repo/$', views.repo, name='repo'),
    url(r'^submit/$', views.submit, name='submit'),
    #ie: /graph/results/5 or /graph/results/21
    url(r'^results/(?P<graph_id>[0-9]+)/$', views.results, name='results'),
    #ie: /graph/about/
    url(r'^about/$', views.about, name='about'),
]