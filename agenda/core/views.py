from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.

def local(request, titulo_evento):
    return HttpResponse(Evento.objects.get(titulo=titulo_evento))

def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválida")    
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    return render(request, 'evento.html')

def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        decricao = request.POST.get('decricao')
        usuario = request.user
        Evento.objects.create(titulo=titulo,
                              data_evento=data_evento,
                              decricao=decricao,
                              usuario=usuario)
    return redirect('/')