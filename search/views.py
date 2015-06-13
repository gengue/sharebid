from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
import json
from django.shortcuts import redirect
from django.contrib import auth
from django.views.generic import View
from .mixins import LoginRequiredMixin
from BeautifulSoup import BeautifulSoup
import requests
from  models import *
import re

class Home(LoginRequiredMixin, View):
    template_name = 'home.html'
    url = "https://www.contratos.gov.co/consultas/resultadosConsulta.do?codi_estado=2&numeroProceso=#"

    def get(self, request):
        ctx ={}
        key_words = tuple([k['name'].lower() for k in request.user.keyword_set.values('name')])
        ctx['key_words'] = serializers.serialize("json", KeyWord.objects.all())
        
        return render(request, self.template_name, ctx)

    def post(self, request):

        r = requests.post(self.url, data={
                'tipoProceso': '1', 'objeto': '10000000',
                'registrosXPagina': '15000', 'cuantia': request.POST.get("cuantia", 0), 'departamento': request.POST.getlist("departamento"), 
                'fechaInicial': request.POST.get("fechaInicial"), 'fechaFinal': request.POST.get("fechaFinal")
            })

        
        
        soup = BeautifulSoup(r.text)

        results = []
        key_words =  request.POST.getlist("key_words[]", None)


        key_words = [k.lower() for k in key_words]
        
            
        for row in soup('table')[0].findAll('tr'):

            tds = row('td')
            words = str(tds[5].string).split(" ")
            
            for word in words:
                word = word.replace("&nbsp;", " ")
                word = re.sub('[,.!#@]', '', word)

                if word.decode('utf-8').lower() in key_words:
                    results.append(self.row_to_dict(row))
                    break

        return render(request, 'results.html', { "results" : results})

    def row_to_dict(self, tr):
        dict = {
            "id": tr('td')[0].string,
            "num_proceso_titulo": tr('td')[1]('a')[0].string,
            "num_proceso_valor": tr('td')[1]('a')[0]['href'],
            "tipo_proceso": tr('td')[2].string,
            "estado": tr('td')[3].string,
            "entidad": tr('td')[4].string,
            "objeto": tr('td')[5].string,
            "lugar": tr('td')[6].text,
            "cuantia": tr('td')[7].string,
            "fecha": tr('td')[8].string
        }
        return dict


class Login(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        print 'aja entro'
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        args = {}

        if user is not None:
            print 'sisa esta bueno'
            if user.is_active:
                auth.login(request, user)
                return redirect("/")
            else:
                args['msg'] = 'El usuario no esta activo'
                return render(request, self.template_name, args)
        else:
            print 'nada que ver'
            args['msg'] = 'El usuario y password son incorrectos'
            return render(request, self.template_name, args)

        return render(request, self.template_name, args)




