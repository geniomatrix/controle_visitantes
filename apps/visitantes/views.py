from django.contrib import messages
from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from visitantes.models import Visitante    
from visitantes.forms import (
    VisitanteForm,AutorizaVisitanteForm,BuscaVisitanteForm
)

from django.utils import timezone
import qrcode
from datetime import timedelta

def identificacao(request):
    # Lógica para criar um QR code
    data = "Dados que você deseja codificar no QR code"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Renderize a página com o QR code
    return render(request, 'identificacao.html', {'img': img})

def buscar_visitante(request):
    visitantes = Visitante.objects.all()
    termo_busca = request.GET.get('termo_busca')
    if termo_busca:
        visitantes = visitantes.filter(nome_completo__icontains=termo_busca)

    form = BuscaVisitanteForm()

    context = {
        'Sócios': visitantes,
        'form': form,
    }

    return render(request, 'buscar_visitante.html', context)



@login_required
def registrar_visitante(request):

    form = VisitanteForm()

    if request.method == "POST":
        form = VisitanteForm(request.POST)
       
        if form.is_valid():
            visitante = form.save(commit=False)
            
            # Calcula a data_final adicionando 2 anos
            
            dois_anos = timedelta(days=365 * 2)
            visitante.validade = timezone.now().date() + dois_anos
            visitante.registrado_por = request.user.porteiro
  
 
            visitante.save()
            messages.success(
                request,
                "Visitante registrado com sucesso"
            )

            return redirect("index")


    context = {
        "nome_pagina": "Registrar visitante",
        "form": form
    }

    return render(request, "registrar_visitante.html", context)

@login_required
def informacoes_visitante(request, id):
    
    visitante = get_object_or_404(
        Visitante,
        id=id
    )

    form = AutorizaVisitanteForm()

    if request.method == "POST":
        form = AutorizaVisitanteForm(
            request.POST,
            instance=visitante
        )

        if form.is_valid():
            visitante = form.save(commit=False)

            visitante.status = "Em Visita"
            visitante.horario_autorizacao = timezone.now()

            visitante.save()
            messages.success(
                request,
                "Entrada de visitante autorizada com sucesso"
            )

            return redirect("index")
        

    context = {
        "nome_pagina": "Informações do sócio",
        "visitante": visitante,
        "form": form
    }

    return render(request, "informacoes_visitante.html", context)

@login_required
def finalizar_visita(request, id):

    if request.method == "POST":
        visitante = get_object_or_404(
            Visitante, id=id
        )

        visitante.status = "FINALIZADO"
        visitante.horario_saida = timezone.now()

        visitante.save()

        messages.success(
            request,
            "Visita finalizada com sucesso"
        )

        return redirect("index")
    else:
        return HttpResponseNotAllowed(
            ["POST"],
            "Método não permitido"
        )

    



        
