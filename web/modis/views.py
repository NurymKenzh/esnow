from django.views import generic
from django.http import HttpResponse
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import subprocess
import datetime
import glob
import os
import ntpath
import shutil
from django.http import JsonResponse
from .models import Source, Product, DataSet, Span
import constants

def index(request):
    context = {}
    template = loader.get_template('modis/index.html')
    return HttpResponse(template.render(context, request))

class SourceListView(generic.ListView):
    template_name = 'modis/source/index.html'
    context_object_name = 'sources'

    def get_queryset(self):
        return Source.objects.all()

class SourceDetailView(generic.DetailView):
    model = Source
    template_name = 'modis/source/detail.html'

class SourceCreateView(CreateView):
    model = Source
    fields = ['name']

class SourceUpdateView(UpdateView):
    model = Source
    fields = ['name']

class SourceDeleteView(DeleteView):
    model = Source
    success_url = reverse_lazy('modis:source')

class ProductListView(generic.ListView):
    template_name = 'modis/product/index.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all()

class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'modis/product/detail.html'

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'source']

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'source']

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('modis:product')

class DataSetListView(generic.ListView):
    template_name = 'modis/dataset/index.html'
    context_object_name = 'datasets'

    def get_queryset(self):
        return DataSet.objects.all()

class DataSetDetailView(generic.DetailView):
    model = DataSet
    template_name = 'modis/dataset/detail.html'

class DataSetCreateView(CreateView):
    model = DataSet
    fields = ['index', 'name', 'data_type',
              'fill_value', 'valid_range', 'product']

class DataSetUpdateView(UpdateView):
    model = DataSet
    fields = ['index', 'name', 'data_type',
              'fill_value', 'valid_range', 'product']

class DataSetDeleteView(DeleteView):
    model = DataSet
    success_url = reverse_lazy('modis:dataset')

class SpanListView(generic.ListView):
    template_name = 'modis/span/index.html'
    context_object_name = 'spans'

    def get_queryset(self):
        return Span.objects.all()

class SpanDetailView(generic.DetailView):
    model = Span
    template_name = 'modis/span/detail.html'

class SpanCreateView(CreateView):
    model = Span
    fields = ['name']

class SpanUpdateView(UpdateView):
    model = Span
    fields = ['name']

class SpanDeleteView(DeleteView):
    model = Span
    success_url = reverse_lazy('modis:span')

def ViewMODIS(request):
    datasets = DataSet.objects.all()
    years = [1, 2, 3, 4]
    context = {
        'datasets': datasets,
        'years': years,
        'geoserver_url': constants.geoserver_url,
        'geoserver_workspace_name': constants.geoserver_workspace_name
    }
    template = loader.get_template('modis/VewMODIS.html')
    return HttpResponse(template.render(context, request))

def GetYears(request):
    if request.method == "GET":
        dataset = DataSet.objects.filter(pk=request.GET.get('dataset_id', None))[0]
        years = []
        for file in glob.glob(constants.geoserver_workspace_folder + "\\" + dataset.product.name + r'\\*.tif'):
            file_date = os.path.splitext(ntpath.basename(file))[0][-7:]
            file_year = file_date[:4]
            years.append(file_year)
        years = list(dict.fromkeys(years))
        data = {
            "message": "Message: " + dataset.name,
            "years": years}
        return JsonResponse(data)
    else:
        return JsonResponse({})

def GetDaysYears(request):
    if request.method == "GET":
        dataset = DataSet.objects.filter(pk=request.GET.get('dataset_id', None))[0]
        year = request.GET.get('year', None)
        daysyears = []
        for file in glob.glob(constants.geoserver_workspace_folder + "\\" + dataset.product.name + r'\\*.tif'):
            file_date = os.path.splitext(ntpath.basename(file))[0][-7:]
            file_year = file_date[:4]
            if file_year == year:
                daysyears.append(file_date[-3:])
        daysyears = list(dict.fromkeys(daysyears))
        data = {
            "message": "Message: OK",
            "daysyears": daysyears}
        return JsonResponse(data)
    else:
        return JsonResponse({})

def GetMODIS(request):
    context = {}
    template = loader.get_template('modis/GetMODIS.html')
    if request.method == 'POST':
        if os.listdir(constants.modis_folder_download):
            return HttpResponse(template.render(context, request))
        spans = ""
        for span in Span.objects.all():
            spans += span.name + ","
        spans = spans[:-1]
        for dataset in DataSet.objects.all():
            year_last = int(constants.modis_first_date[:4])
            month_last = int(constants.modis_first_date[:7][-2:])
            day_last = int(constants.modis_first_date[-2:]) - 1
            day_of_year_last = (
                datetime.datetime(year=year_last, month=month_last, day=day_last)
                - datetime.datetime(year_last, 1, 1)).days + 1
            for file in glob.glob(constants.geoserver_workspace_folder + "\\" + dataset.product.name + r'\\*.tif'):
                file_date = os.path.splitext(ntpath.basename(file))[0][-7:]
                file_year = file_date[:4]
                file_day_of_year = file_date[-3:]
                if int(file_year) >= year_last and int(file_day_of_year) >= day_of_year_last:
                    year_last = int(file_year)
                    day_of_year_last = int(file_day_of_year)
            date_last = datetime.datetime(year_last, 1, 1) + datetime.timedelta(day_of_year_last)

            proc_download =\
                subprocess.Popen("cmd.exe /c modis_download.py -U "
                                 + constants.modis_user
                                 + " -P "
                                 + constants.modis_password
                                 + " -r -u https://n5eil01u.ecs.nsidc.org -s "
                                 + dataset.product.source.name
                                 + " -p "
                                 + dataset.product.name
                                 + " -t "
                                 + spans
                                 + " -f "
                                 + date_last.strftime("%Y-%m-%d")
                                 + " -e "
                                 + datetime.datetime.now().strftime("%Y-%m-%d")
                                 # + "2018-12-31"
                                 + " "
                                 + constants.modis_folder_download,
                                 cwd=constants.modis_folder_download,
                                 shell=True)
            proc_download.wait()
            proc_mosaic =\
                subprocess.Popen(r"cmd.exe /c modis_mosaic.py -o "
                                 + constants.modis_filename_mosaic
                                 + r" -s " + "\""
                                 + str(dataset.index)
                                 + "\" "
                                 + constants.modis_folder_download
                                 + r"\listfile"
                                 + dataset.product.name
                                 + r".txt",
                                 cwd=constants.modis_folder_download,
                                 shell=True)
            proc_mosaic.wait()

            if not os.path.exists(constants.geoserver_workspace_folder
                    + "\\"
                    + dataset.product.name):
                os.makedirs(constants.geoserver_workspace_folder
                    + "\\"
                    + dataset.product.name)

            for file in glob.glob(constants.modis_folder_download + r'\\*.tif'):
                proc_reproject = subprocess.Popen(
                    r"cmd.exe /c modis_convert.py -v -s " + "\"( "
                    + str(dataset.index)
                    + " )\"" + r" -o "
                    + dataset.name + r"_" + os.path.splitext(ntpath.basename(file))[0][:-1]
                    + r" -e "
                    + constants.modis_projection
                    + r" "
                    + file,
                    cwd=constants.modis_folder_download,
                    shell=True)
                proc_reproject.wait()
                shutil.move(
                    constants.modis_folder_download
                    + "\\"
                    + dataset.name
                    + r"_"
                    + os.path.splitext(ntpath.basename(file))[0][:-1] + ".tif",
                    constants.geoserver_workspace_folder
                    + "\\"
                    + dataset.product.name
                    + "\\"
                    + dataset.name
                    + r"_"
                    + os.path.splitext(ntpath.basename(file))[0][:-1] + ".tif")

                proc_publish_store = subprocess.Popen(
                    r"cmd.exe /c curl -v -u "
                    + constants.geoserver_user
                    + r":"
                    + constants.geoserver_password
                    + r" -POST -H "
                    + "\"Content-type: text/xml\" -d \"<coverageStore><name>"
                    + dataset.name
                    + r"_"
                    + os.path.splitext(ntpath.basename(file))[0][:-1]
                    + "</name><type>GeoTIFF</type><enabled>true</enabled><workspace>"
                    + constants.geoserver_workspace_name
                    + "</workspace><url>/data/"
                    + constants.geoserver_workspace_name
                    + "/"
                    + dataset.product.name
                    + "/"
                    + dataset.name
                    + r"_"
                    + os.path.splitext(ntpath.basename(file))[0][:-1] + ".tif"
                    + "</url></coverageStore>\" "
                    + constants.geoserver_url
                    + "/geoserver/rest/workspaces/"
                    + constants.geoserver_workspace_name
                    + "/coveragestores?configure=all",
                    cwd=constants.geoserver_workspace_folder,
                    shell=True)
                proc_publish_store.wait()
                proc_publish_layer = subprocess.Popen(
                    r"cmd.exe /c curl -v -u "
                    + constants.geoserver_user
                    + r":"
                    + constants.geoserver_password
                    + " -PUT -H \"Content-type: text/xml\" -d \"<coverage><name>"
                    + dataset.name
                    + r"_"
                    + os.path.splitext(ntpath.basename(file))[0][:-1]
                    + "</name><title>"
                    + dataset.name
                    + r"_"
                    + os.path.splitext(ntpath.basename(file))[0][:-1]
                    + "</title><defaultInterpolationMethod><name>nearest neighbor</name></defaultInterpolationMethod><srs>"
                    + constants.geoserver_projection
                    + "</srs></coverage>\" \""
                    + constants.geoserver_url
                    + "/geoserver/rest/workspaces/"
                    + constants.geoserver_workspace_name
                    + "/coveragestores/"
                    + dataset.name
                    + r"_"
                    + os.path.splitext(ntpath.basename(file))[0][:-1]
                    + "/coverages?recalculate=nativebbox\"",
                    cwd=constants.geoserver_workspace_folder,
                    shell=True)
                proc_publish_layer.wait()
                proc_publish_style = subprocess.Popen(
                    r"cmd.exe /c curl -v -u "
                    + constants.geoserver_user
                    + r":"
                    + constants.geoserver_password
                    + " -X PUT -H \"Content-type: text/xml\" -d \"<layer><defaultStyle><name>"
                    + constants.geoserver_workspace_name
                    + ":"
                    + dataset.name
                    + "</name></defaultStyle></layer>\" "
                    + constants.geoserver_url
                    + "/geoserver/rest/layers/"
                    + constants.geoserver_workspace_name
                    + ":"
                    + dataset.name
                    + r"_"
                    + os.path.splitext(ntpath.basename(file))[0][:-1],
                    cwd=constants.geoserver_workspace_folder,
                    shell=True)
                proc_publish_style.wait()

            # for file in os.listdir(constants.modis_folder_download):
            #     file_path = os.path.join(constants.modis_folder_download, file)
            #     if os.path.isfile(file_path):
            #         os.unlink(file_path)
    return HttpResponse(template.render(context, request))