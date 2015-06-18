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
import urllib

class Home(LoginRequiredMixin, View):
    template_name = 'home.html'
    
    url = "https://www.contratos.gov.co/consultas/resultadosConsulta.do"
    # http://www.contratos.gov.co/consultas/resultadosConsulta.do?&departamento=5000&paginaObjetivo=1&cuantia=0&fechaInicial=&ctl00$ContentPlaceHolder1$hidRangoMaximoFecha=&desdeFomulario=true&fechaFinal=&objeto=&tipoProceso=1&registrosXPagina=50&numeroProceso=&municipio=0&estado=0
    def get(self, request):
        ctx ={}
        key_words = tuple([k['name'].lower() for k in request.user.keyword_set.values('name')])
        ctx['key_words'] = serializers.serialize("json", KeyWord.objects.all())
        
        return render(request, self.template_name, ctx)

    def post(self, request):

        payload = {
        'departamento': request.POST.get('departamento'),
        'paginaObjetivo': '1',
        'cuantia':request.POST.get('cuantia'),
        'fechaInicial': request.POST.get('fechaInicial'),
        'ctl00$ContentPlaceHolder1$hidRangoMaximoFecha':'',
        'desdeFomulario':'true',
        'fechaFinal':request.POST.get('fechaFinal'),
        'tipoProceso': request.POST.get('tipoProceso'),
        'registrosXPagina':'50',
        'numeroProceso':'',
        'municipio':'0',
        'estado': '0',                                  
        }                                           
        #payload = {'departamento': '5000','paginaObjetivo': '1','cuantia':'0','fechaInicial':'','ctl00$ContentPlaceHolder1$hidRangoMaximoFecha':'','desdeFomulario':'true','fechaFinal':'','tipoProceso':'1','registrosXPagina':'50','numeroProceso':'','municipio':'0','estado': '0',}                                                                                                   
        print '*'*100
        print payload
        print '*'*100
        
        if request.POST.get('departamento') == "" and request.POST.get('fechaInicial') == "" and request.POST.get('fechaFinal') == "" and request.POST.get('tipoProceso') == "" and request.POST.get('cuantia') == '0':
           payload.clear()

        print '*'*100          
        print payload
        print '*'*100

        
        
        params = urllib.urlencode(payload)
        r = urllib.urlopen("http://www.contratos.gov.co/consultas/resultadosConsulta.do",params)
        
        
            
        soup = BeautifulSoup(r.read())

        results = []
        key_words =  request.POST.getlist("key_words[]", None)
        key_words = [k.lower() for k in key_words]
        
        
        
            
        for row in soup('table')[0].findAll('tr'):
            tds = row('td')
            words = str(tds[5].string).split(" ")

            for word in words:
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
            "fecha": tr('td')[8].text,
        }
        return dict


class Login(View):

    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        args = {}

        if user is not None:
            
            if user.is_active:
                auth.login(request, user)
                return redirect("/")
            else:
                args['msg'] = 'El usuario no esta activo'
                return render(request, self.template_name, args)
        else:
            
            args['msg'] = 'El usuario y password son incorrectos'
            return render(request, self.template_name, args)

        return render(request, self.template_name, args)




