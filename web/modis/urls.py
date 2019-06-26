# git test

from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import user_passes_test

app_name = 'modis'

urlpatterns = [
    # /modis/
    url(r'^$', (user_passes_test(lambda u: u.is_staff))(views.index), name='index'),

    # /modis/source/
    url(r'source/$', (user_passes_test(lambda u: u.is_staff))(views.SourceListView.as_view()), name='source'),

    # /modis/source/712/
    url(r'^source/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.SourceDetailView.as_view()), name='source_detail'),

    # /modis/source/create/
    url(r'source/create/$', (user_passes_test(lambda u: u.is_staff))(views.SourceCreateView.as_view()), name='source_create'),

    # /modis/source/update/712/
    url(r'^source/update/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.SourceUpdateView.as_view()), name='source_update'),

    # /modis/source/delete/712/
    url(r'^source/delete/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.SourceDeleteView.as_view()), name='source_delete'),

    # /modis/product/
    url(r'product/$', (user_passes_test(lambda u: u.is_staff))(views.ProductListView.as_view()), name='product'),

    # /modis/product/712/
    url(r'^product/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.ProductDetailView.as_view()), name='product_detail'),

    # /modis/product/create/
    url(r'product/create/$', (user_passes_test(lambda u: u.is_staff))(views.ProductCreateView.as_view()), name='product_create'),

    # /modis/product/update/712/
    url(r'^product/update/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.ProductUpdateView.as_view()), name='product_update'),

    # /modis/product/delete/712/
    url(r'^product/delete/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.ProductDeleteView.as_view()), name='product_delete'),

    # /modis/dataset/
    url(r'dataset/$', (user_passes_test(lambda u: u.is_staff))(views.DataSetListView.as_view()), name='dataset'),

    # /modis/dataset/712/
    url(r'^dataset/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.DataSetDetailView.as_view()), name='dataset_detail'),

    # /modis/dataset/create/
    url(r'dataset/create/$', (user_passes_test(lambda u: u.is_staff))(views.DataSetCreateView.as_view()), name='dataset_create'),

    # /modis/dataset/update/712/
    url(r'^dataset/update/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.DataSetUpdateView.as_view()), name='dataset_update'),

    # /modis/dataset/delete/712/
    url(r'^dataset/delete/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.DataSetDeleteView.as_view()), name='dataset_delete'),

    # /modis/span/
    url(r'span/$', (user_passes_test(lambda u: u.is_staff))(views.SpanListView.as_view()), name='span'),

    # /modis/span/712/
    url(r'^span/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.SpanDetailView.as_view()), name='span_detail'),

    # /modis/span/create/
    url(r'span/create/$', (user_passes_test(lambda u: u.is_staff))(views.SpanCreateView.as_view()), name='span_create'),

    # /modis/span/update/712/
    url(r'^span/update/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.SpanUpdateView.as_view()), name='span_update'),

    # /modis/span/delete/712/
    url(r'^span/delete/(?P<pk>[0-9]+)/$', (user_passes_test(lambda u: u.is_staff))(views.SpanDeleteView.as_view()), name='span_delete'),

    # /modis/getmodis
    url(r'getmodis/$', (user_passes_test(lambda u: u.is_staff))(views.GetMODIS), name='getmodis'),

    # /modis/viewmodis
    url(r'viewmodis/$', (user_passes_test(lambda u: u.is_staff))(views.ViewMODIS), name='viewmodis'),

    # /modis/getyears
    url(r'getyears/$', (user_passes_test(lambda u: u.is_staff))(views.GetYears), name='getyears'),

    # /modis/getdaysyears
    url(r'getdaysyears/$', (user_passes_test(lambda u: u.is_staff))(views.GetDaysYears), name='getdaysyears'),
]
