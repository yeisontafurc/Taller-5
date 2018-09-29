from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from collections import namedtuple
import json
from .classes.DFuntional import DFuncional
from .classes.RecubrimientoMinimo import RecubrimientoMinimo
from .classes.Util import Util
from .classes.CalculoLlaves import CalculoLlaves
from .classes.FormasNormales import FormasNormales
from .controllers.MapaAlfabeto import MapaAlfabeto
from .controllers.Respuesta import Respuesta
from .classes.Elemento import elemento

def index(request):
    latest_question_list = range(5)
    latest_question_list = ["{:02d}".format(x) for x in latest_question_list]
    template = loader.get_template('polls/form.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


@csrf_exempt
def detail(request, question_id):
    postgetted = request.POST.get("title", question_id)
    return HttpResponse("You're looking at question %s." % postgetted)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    print(request)
    return HttpResponse(response % question_id)


def vote(request, question_id):
    print(request)
    return HttpResponse("You're voting on question %s." % question_id)


@csrf_exempt
def manual(request):
    postgetted = request.POST.get("json_atributos", "")
    #dependencias_from_form = decodificarJson(postgetted)
    alfabeto_from_form = request.POST.get("atributos", "")
    #ALFABETO FROM FORM está separado por comas
    lista_alfabeto = alfabeto_from_form.split(",")
    mapa = MapaAlfabeto(lista_alfabeto,[])
    alfabeto_con_comas_arreglo = mapa.crearMapa()
    dependencias_from_form = decodificarJson(postgetted, mapa)
    alfabeto_con_comas = ""
    booliefo = True
    for letra in alfabeto_con_comas_arreglo:
        if booliefo:
            alfabeto_con_comas = letra.key
            booliefo = False
        else:
            alfabeto_con_comas = alfabeto_con_comas + "," + letra.key


    respuestas = []
    recubrimiento = RecubrimientoMinimo(dependencias_from_form)
    L1 = recubrimiento.caclular_l1()
    Util.imprimirListaDependencias(L1, "Recubrimiento etapa L1")
    respuesta = Respuesta(formatearLista(L1,mapa),"Recubrimiento minimo etapa L1")
    respuestas.append(respuesta)

    recubrimiento.set_lista_df(L1)
    L2 = recubrimiento.calcular_l2()
    Util.imprimirListaDependencias(L2, "Recubrimiento etapa L2")
    respuesta = Respuesta(formatearLista(L2,mapa), "Recubrimiento minimo etapa L2")
    respuestas.append(respuesta)

    L3 = recubrimiento.calcular_l3(L2)
    Util.imprimirListaDependencias(L3, "Recubrimiento etapa L3")
    respuesta = Respuesta(formatearLista(L3,mapa), "Recubrimiento minimo etapa L3")
    respuestas.append(respuesta)

    lista_alfabeto = alfabeto_con_comas.split(",")
    Util.imprimirListaDependencias(lista_alfabeto, "A L F A B E T O")
    respuesta = Respuesta(alfabeto_from_form.split(","), "A L F A B E T O")
    respuestas.append(respuesta)
    m1 = set()
    m2 = set()
    calculoLlave = CalculoLlaves(L3, lista_alfabeto, m1, m2)
    calculoLlave.llaveCandidata()
    Util.imprimirListaDependencias(calculoLlave.get_m2(), "Llaves candidatas")
    respuesta = Respuesta(formatearLista(calculoLlave.get_m2(),mapa), "Llaves candidatas")
    respuestas.append(respuesta)

    formaNormal = FormasNormales(calculoLlave.get_m2(), L3, True)
    if formaNormal.verificarSegundaFN():
        print("Está en segunda forma normal")
        respuesta = Respuesta([], "Está en segunda forma normal")
        respuestas.append(respuesta)
    else:
        print("No está en segunda forma normal")
        respuesta = Respuesta([], "No está en segunda forma normal")
        respuestas.append(respuesta)
    if formaNormal.verificarTerceraFN():
        print("Está en tercera forma normal")
        respuesta = Respuesta([], "Está en tercera forma normal")
        respuestas.append(respuesta)
    else:
        print("No está en tercera forma normal")
        respuesta = Respuesta([], "No está en tercera forma normal")
        respuestas.append(respuesta)
    if formaNormal.verificarFNBC():
        print("Está en forma normal boyce-codd")
        respuesta = Respuesta([], "Está en normal boyce-codd")
        respuestas.append(respuesta)
    else:
        print("No está en forma normal boyce-codd")
        respuesta = Respuesta([], "Está en normal boyce-codd")
        respuestas.append(respuesta)

    template = loader.get_template('polls/resultado.html')

    for rtas in respuestas:
        print(rtas.titulo)
        print(rtas.lista)

    context = {
            'respuestas': respuestas ,
    }
    return HttpResponse ( template.render ( context , request ) )


@csrf_exempt
def jsonupload(request):
    postgetted = 'There\'s no files'
    if request.method == 'POST':
        if not (request.FILES is None):
            try:
                if request.FILES['element_4'].name.find(".json") == -1:
                    postgetted = "No es un archivo .json"
                else:
                    postgetted = request.FILES['element_4'].read()
                    print(''.join(decodificarJson(postgetted.decode("utf-8"))))
            except Exception as inst:
                postgetted = "Se presentó el error:  " + type(inst).__name__ + ":   " + ''.join(inst.args)
    else:
        postgetted = 'There\'s no files'
    return HttpResponse("You're looking at nothing %s." % postgetted)


def decodificarJson(json_string: str, mapa):
    carga = json.loads(json_string)
    entradaStr = json.dumps(carga)
    y = json.loads(entradaStr, object_hook=lambda d: namedtuple('r', d.keys())(*d.values()))
    dependencias = y.dFuncionales
    L = []
    for x in dependencias:
        implicante = x.x
        implicado = x.y
        if(len(x.x.split(",")) > 1):
            implicante = ""
            implicantes = x.x.split(",")
            for im in implicantes:
                implicante = implicante + mapa.obtenerChar(im)
        else:
            implicante = mapa.obtenerChar(implicante)

        if (len(x.y.split(",")) > 1):
            implicado = ""
            implicados = x.y.split(",")
            for im in implicados:
                implicado = implicado + mapa.obtenerChar(im)
        else:
            implicado = mapa.obtenerChar(implicado)

        depAux = DFuncional(implicante, implicado)

        L.append(depAux)
    return L

def formatearLista(lista:[],mapa):
    lista_printeable = []
    if(len(lista) > 0):
        for elementosLista in lista:
            if(type(elementosLista) is DFuncional):
                string = '{{"{0}"->"{1}"}}'.format( mapa.obtenerStringFromChar(elementosLista.x), mapa.obtenerStringFromChar(elementosLista.y))
                lista_printeable.append(string)
            elif type(elementosLista) is elemento:
                string = '{0}'.format(mapa.obtenerStringFromChar(elementosLista.y))
                lista_printeable.append(string)
            else:
                string = mapa.obtenerStringFromChar(elementosLista)
                lista_printeable.append(string)
    return lista_printeable