from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Page_Layout, name='index'),
    # url(r'^$', views.Rating_line_bar, name='index'),
    # url(r'^$', views.Rating_Pie, name='index'),
    # url(r'^$', views.Rating_Pie, name='index'),
    # url(r'^$', views.Rating_Pie, name='index'),
]