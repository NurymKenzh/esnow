from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import user_passes_test

app_name = 'coordinates'

urlpatterns = [
    # /coordinates/
    url(r'^$', views.index, name='index'),

    # /coordinates/coordinatesystem/
    url(r'coordinatesystem/$', (user_passes_test(lambda u: u.is_staff))(views.CoordinateSystemListView.as_view()), name='coordinatesystem'),

    # /coordinates/coordinatesystem/712/
    url(r'^coordinatesystem/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.CoordinateSystemDetailView.as_view()), name='coordinatesystem_detail'),

    # /coordinates/coordinatesystem/create/
    url(r'coordinatesystem/create/$', (user_passes_test(lambda u: u.is_staff))(views.CoordinateSystemCreateView.as_view()), name='coordinatesystem_create'),

    # /coordinates/coordinatesystem/update/712/
    url(r'^coordinatesystem/update/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.CoordinateSystemUpdateView.as_view()), name='coordinatesystem_update'),

    # /coordinates/coordinatesystem/delete/712/
    url(r'^coordinatesystem/delete/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.CoordinateSystemDeleteView.as_view()), name='coordinatesystem_delete'),
]