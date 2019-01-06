from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView, TemplateView
from service.models import FOAAS, APIEndPoint
from django.http import HttpResponse
from django.urls import reverse_lazy
from service.form.forms import FOAASForm
from django import forms
from django.shortcuts import redirect
import requests

# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_endpoints'] = APIEndPoint.objects.all()
        return context

class FOAASListView(ListView):
    template_name = 'foaas_list.html'
    model = FOAAS

class FOAASCreateView(CreateView):
    form_class = FOAASForm
    template_name = 'foaas_message_create.html'
    model = FOAAS

    success_url = ""


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if(self.request.method == "GET"):
            api_endpoint = APIEndPoint.objects.get(id = self.request.GET.get('endpoint'))
            boxes = {
                'box_1': '',
                'box_2': '',
                'box_3': ''
            }
            box_count = 0
            for field in eval(api_endpoint.fields):
                box_count += 1
                box = f'box_{box_count}'
                boxes[box] = field
                setattr(context['form'].fields[box], 'label', field['name'])
            context['api_endpoint_id'] = self.request.GET.get('endpoint')
            
            if(box_count < 3):
                for number in range(3 - box_count):
                    box_count += 1
                    box = f'box_{box_count}'
                    del(context['form'].fields[box])
        return context

    def form_valid(self, form):
        message = form.save()
        api_endpoint = APIEndPoint.objects.get(id = self.request.POST.get('endpoint'))
        boxes = {
            'box_1': '',
            'box_2': '',
            'box_3': ''
        }
        box_count = 0
        for field in api_endpoint.get_fields():
            box_count += 1
            box = f'box_{box_count}'
            boxes[box] = field
        self.message_url = f'http://www.foaas.com' + api_endpoint.url
        count = 1
        while(count < 4):
            box = f'box_{count}'
            if box in self.request.POST:
                add = self.request.POST.get(f'box_{count}')
                print(add)
                self.message_url = self.message_url.replace(f':{boxes[box]}', add)
            count +=1
        headers = {'Accept': 'text/plain'}
        message.foaas_message = requests.get(f'{self.message_url}', headers=headers).text
        return super().form_valid(form)


class FOAASDetailView(DetailView):
    template_name = 'FOAAS_detail.html'
    model = FOAAS


class FOAASDeleteView(DeleteView):
    model = FOAAS
    template_name = 'foaas_delete.html'
    success_url = reverse_lazy('FOAAS_list')
    

class FOAASUpdateView(UpdateView):
    model = FOAAS
    fields = ['box_1', 'box_2', 'box_3']