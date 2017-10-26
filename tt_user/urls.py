from django.conf.urls import url
from tt_user import views
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^register_handle/$', views.register_handle, name='register_handle'),
    url(r'^check_user_exist/$', views.check_user_exist, name='check_user_exist'),
    url(r'^active/(.*)/$', views.register_active, name='active'),

    url(r'^login/$', views.login, name='login'),
    url(r'^login_check/$', views.login_check, name='login_check'),
    url(r'^logout/$', views.logout, name='logout'),
    # url(r'^send/$', views.send, name='send'),
    url(r'^$', views.user, name='user'),
    url(r'^order/$', views.order, name='order'),
    url(r'^address/$', views.address, name='address'),
    url(r'^address_handle/$', views.address_handle, name='address_handle'),


]
