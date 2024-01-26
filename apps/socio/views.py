# socios/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Socio, Dependentes
from .forms import SocioForm, DependenteForm,BuscaSocioForm,SocioSearchForm
from datetime import timedelta
from django.utils import timezone


def lista_socios(request):
    socio = Socio.objects.all()
    return render(request, 'lista_socios.html', {'socio': socio})

def detalhes_socio(request, socio_id):
    socio = get_object_or_404(Socio, pk=socio_id)
 
    dependente_form = DependenteForm()
    dois_meses = timedelta(days=60)
    if request.method == 'POST':
        dependente_form = DependenteForm(request.POST)
        if dependente_form.is_valid():
            dependente = dependente_form.save(commit=False)
            dependente.socio = socio
            if dependente.filiacao == "ESPOSA(o)":
                dois_anos = timedelta(days=365 * 10)
                dependente.validade = timezone.now().date() + dois_anos
            elif dependente.filiacao == "FILHO(a)":
                dois_anos = timedelta(days=365 * 5)
                dependente.validade = timezone.now().date() + dois_anos                    
            else:
                dois_anos = timedelta(days=365 * 3)
                dependente.validade = timezone.now().date() + dois_anos                    
            dependente.dtexame_fin = timezone.now().date() + dois_meses
            existe_registros = Dependentes.objects.exists()
            if existe_registros:  
                ultimo_registro = Dependentes.objects.latest('id')
                proximo_registro = ultimo_registro.id + 1 
                dependente.nrcart = "D"+str(proximo_registro)+str(socio_id)+socio.tpsocio
                dependente.save()
            else:
                dependente.nrcart = "D"+str(1)+str(socio_id)+socio.tpsocio
                dependente.save()

            return redirect('detalhes_socio', socio_id=socio_id)

    return render(request, 'detalhes_socio.html', {'socio': socio, 'dependente_form': dependente_form})

def buscar_socio(request):
    socio_id = None
    if request.method == 'POST':
        form = BuscaSocioForm(request.POST)
        if form.is_valid():
            #socio_id = form.cleaned_data['socio_id']
            nrcart = form.cleaned_data['nrcart']
            try:
                #socio = Socio.objects.get(pk=socio_id)
                socio = Socio.objects.get(nrcart=nrcart)
                socio_id = socio.id
                return render(request, 'detalhes_sociocart.html', {'socio': socio,'socio_id': socio_id})
                #return redirect('detalhes_socio', socio_id=socio_id)
            except Socio.DoesNotExist:
                try:
                    dependente = Dependentes.objects.get(nrcart=nrcart)
                    socio = dependente.socio
                    socio_id = socio.id
                    return render(request, 'detalhes_dependente.html', {'dependente': dependente,'socio': socio, 'socio_id': socio_id})

                except Dependentes.DoesNotExist:
                    mensagem = 'Sócio e dependente não encontrado.'.format(nrcart)
                    return render(request, 'registrone.html', {'mensagem': mensagem, 'form': form})
    else:
        form = BuscaSocioForm()

    return render(request, 'buscar_socio_acesso.html', {'form': form})

def search_socio(request):
    form = SocioSearchForm(request.GET)
    results = []
 

    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        
        results = Socio.objects.filter(nrcart__icontains=search_query)
    return render(request, 'search_results.html', {'form': form, 'results': results})  
 
def cadastrar_socio(request):
    if request.method == 'POST':
        form = SocioForm(request.POST)
        if form.is_valid():
            existe_registros = Socio.objects.exists()
            if existe_registros:  
                ultimo_registro = Socio.objects.latest('id')
                proximo_registro = ultimo_registro.id + 1 
                dois_meses = timedelta(days=60)
                form.instance.dtexame_fin = timezone.now().date() + dois_meses
                form.instance.nrcart = "S"+str(proximo_registro)+form.instance.tpsocio 
                form.save()
            else:
                dois_meses = timedelta(days=60)
                form.instance.dtexame_fin = timezone.now().date() + dois_meses
                form.instance.nrcart = "S"+str(1)+form.instance.tpsocio 
                form.save()
            return redirect('lista_socios')
    else:
        form = SocioForm()
    return render(request, 'cadastrar_socio.html', {'form': form})

def editar_socio(request, pk):
    socio = get_object_or_404(Socio, pk=pk)
    if request.method == 'POST':
        form = SocioForm(request.POST, instance=socio)
        if form.is_valid():
            form.save()
            return redirect('lista_socios')
    else:
        form = SocioForm(instance=socio)
    return render(request, 'editar_socio.html', {'form': form})

def excluir_socio(request, pk):
    socio = get_object_or_404(Socio, pk=pk)
    socio.delete()
    return redirect('lista_socios')