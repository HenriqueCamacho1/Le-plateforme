from django.shortcuts import render
from django.http import JsonResponse

from django.core.files.storage import FileSystemStorage
from rebecca import motor, write


import os
import json

PATH = "file.xlsx"


# --- VIEWS
def encarregado(request):
    return render(request, 'rebecca/encarregado.html')

def trelas(request):

    if request.method == 'GET' and len(request.GET) > 0:
        
        if ('input1' not in request.GET) or ('input2' not in request.GET) or ('input3' not in request.GET):
            return render(request, 'rebecca/trelas.html', {'error': 'notfound'})

        if (request.GET['input1'] == '') or (request.GET['input2'] == '') or (request.GET['input3'] == ''):
            return render(request, 'rebecca/trelas.html', {'error': 'notfound'})

        if not existeExcel():
            return render(request, 'rebecca/trelas.html', {'error' : 'excelNotLoaded'})

        motor.ini()
        sup, inf = motor.procurar(request.GET['input1'],request.GET['input2'],request.GET['input3'])

        # if sup == -1 or inf == -1:
        #     return render(request, 'rebecca/trelas.html', {'error', 'notfound'})

        if sup == None or inf == None:
            return render(request, 'rebecca/trelas.html', {'error': 'notfound'})

        return render(request, 'rebecca/trelas.html', {'sup': sup, 'inf': inf})

    print("No query params, normal page load")
    return render(request, 'rebecca/trelas.html')

# -------------------------------------------------------

def modificar(request):

    


    return render(request, 'rebecca/modificar.html')


def getOrdemData(request):

    data = motor.get_table_ordem()

    return JsonResponse({'result': data})


def getGruasData(request):

    data = motor.get_table_gruas()

    return JsonResponse({'result': data})

def getHoraData(request):

    data = motor.get_table_hora()

    return JsonResponse({'result': data})


# --- ACTIONS

# POST
def upload(request):

    if  len(request.FILES) <= 0:
        return render(request, 'rebecca/encarregado.html')


    if request.method == 'POST' and request.FILES['myfile']:

        if existeExcel():
            os.remove(PATH)

        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        fs.save(PATH, myfile)
        
        motor.ini()
      
    return render(request, 'rebecca/encarregado.html')


def updateData(request):

    if request.method == 'POST':

        jsonObj = json.loads(request.POST['body'])

        table = jsonObj['tabela']
        list = jsonObj['data']

        if table == 'ordem': write.write_ordem(list)
        if table == 'gruas': write.write_grua(list)
        if table == 'hora': write.write_hora(list)


    return render(request, 'rebecca/modificar.html')


# GET
def procurar(request):

    

    return render(request, 'rebecca/trelas.html', {'error' : 'internalerror'})

# -------------------------------------------------------


# PRIVATE FUNCTIONS

def existeExcel():
    return os.path.exists(PATH)



# -------------------------------------------------------