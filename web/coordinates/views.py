from django.views import generic
from django.http import HttpResponse
from django.template import loader
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import CoordinateSystem

def index(request):
    context = {}
    template = loader.get_template('coordinates/index.html')
    return HttpResponse(template.render(context, request))

class CoordinateSystemListView(generic.ListView):
    template_name = 'coordinates/coordinatesystem/index.html'
    context_object_name = 'coordinatesystems'

    def get_queryset(self):
        return CoordinateSystem.objects.all()

class CoordinateSystemDetailView(generic.DetailView):
    model = CoordinateSystem
    template_name = 'coordinates/coordinatesystem/detail.html'

class CoordinateSystemCreateView(CreateView):
    model = CoordinateSystem
    fields = ['name']

class CoordinateSystemUpdateView(UpdateView):
    model = CoordinateSystem
    fields = ['name']

class CoordinateSystemDeleteView(DeleteView):
    model = CoordinateSystem
    success_url = reverse_lazy('coordinates:coordinatesystem')