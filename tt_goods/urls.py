from django.conf.urls import url
from tt_goods import views
urlpatterns = [
    url(r'^$', views.index, name='index')
]
