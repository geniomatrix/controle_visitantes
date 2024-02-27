# socios/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Socio, Dependentes
from .forms import SocioForm, DependenteForm,BuscaSocioForm,SocioSearchForm,DependenteSearchForm
from datetime import timedelta
from django.utils import timezone
from .utils import preencher_endereco_por_cep



def lista_socios(request):
    #socio = Socio.objects.all() #Socio.objects.filter(ativo='Sim')
    #return render(request, 'lista_socios.html', {'socio': socio})
    form = SocioSearchForm(request.GET)
    socios = Socio.objects.all()

    if form.is_valid():
        search_term = form.cleaned_data['search_term']
        #socios = socios.filter(nome__icontains=search_term) | socios.filter(registro__icontains=search_term)
        socios = socios.filter(nome__icontains=search_term)

    context = {'socio': socios, 'form': form}
    return render(request, 'lista_socios.html', context)

def lista_socios_altera(request):
    #socio = Socio.objects.all() #Socio.objects.filter(ativo='Sim')
    #return render(request, 'lista_socios.html', {'socio': socio})
    form = SocioSearchForm(request.GET)
    socios = Socio.objects.all()

    if form.is_valid():
        search_term = form.cleaned_data['search_term']
        #socios = socios.filter(nome__icontains=search_term) | socios.filter(registro__icontains=search_term)
        socios = socios.filter(nome__icontains=search_term)

    context = {'socio': socios, 'form': form}
    return render(request, 'lista_socios_altera.html', context)

def lista_dependentes(request):

    form = DependenteSearchForm(request.GET)
    dependentes = Dependentes.objects.all()

    if form.is_valid():
        search_term = form.cleaned_data['search_term']
        #socios = socios.filter(nome__icontains=search_term) | socios.filter(registro__icontains=search_term)
        dependentes = dependentes.filter(nome__icontains=search_term)

    context = {'dependentes': dependentes, 'form': form}
    return render(request, 'lista_dependentes.html', context)

def lista_dependentes_altera(request):

    form = DependenteSearchForm(request.GET)
    dependentes = Dependentes.objects.all()

    if form.is_valid():
        search_term = form.cleaned_data['search_term']
        #socios = socios.filter(nome__icontains=search_term) | socios.filter(registro__icontains=search_term)
        dependentes = dependentes.filter(nome__icontains=search_term)

    context = {'dependentes': dependentes, 'form': form}
    return render(request, 'lista_dependentes_altera.html', context)

def detalhes_socio(request, socio_id):
    socio = get_object_or_404(Socio, pk=socio_id)
 
    dependente_form = DependenteForm()
    dois_meses = timedelta(days=60) #validade do exame medico
    if request.method == 'POST':
        dependente_form = DependenteForm(request.POST)
        if dependente_form.is_valid():
            dependente = dependente_form.save(commit=False)
            dependente.socio = socio
            #valida conforme filiação
            if dependente.filiacao == "FILHO(a)":
                qtd_anos = timedelta(days=365 * 25)
                #dependente.validade = timezone.now().date() + qtd_anos
                dependente.validade = dependente.data_nascimento + qtd_anos
            elif dependente.filiacao == "NETO(a)":
                qtd_anos = timedelta(days=365 * 12)
                #dependente.validade = timezone.now().date() + qtd_anos
                dependente.validade = dependente.data_nascimento + qtd_anos
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

def detalhes_dependente(request, dependente_id):
    dependente = get_object_or_404(Dependente, pk=dependente_id)
 
    dependente_form = DependenteForm()
    dois_meses = timedelta(days=60) #validade do exame medico
    if request.method == 'POST':
        dependente_form = DependenteForm(request.POST)
        if dependente_form.is_valid():
            dependente = dependente_form.save(commit=False)
            dependente.socio = socio
            #valida conforme filiação
            if dependente.filiacao == "FILHO(a)":
                qtd_anos = timedelta(days=365 * 25)
                #dependente.validade = timezone.now().date() + qtd_anos
                dependente.validade = dependente.data_nascimento + qtd_anos
            elif dependente.filiacao == "NETO(a)":
                qtd_anos = timedelta(days=365 * 12)
                #dependente.validade = timezone.now().date() + qtd_anos
                dependente.validade = dependente.data_nascimento + qtd_anos
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

            return redirect('detalhes_dependente', dependente_id=dependente_id)

    return render(request, 'detalhes_dependente.html', {'dependente': dependente, 'dependente_form': dependente_form})



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
            cep = form.cleaned_data['cep']
            endereco = preencher_endereco_por_cep(cep)
            if endereco:
                form.instance.logradouro = endereco['logradouro']
                form.instance.bairro = endereco['bairro']
                form.instance.cidade = endereco['cidade']
                form.instance.estado = endereco['estado']
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
        dois_meses = timedelta(days=60) #validade do exame medico
        if form.is_valid():
            socio.dtexame_fin = timezone.now().date() + dois_meses
            form.save()
            return redirect('lista_socios_altera')
    else:
        form = SocioForm(instance=socio)
    return render(request, 'editar_socio.html', {'form': form})

def excluir_socio(request, pk):
    socio = get_object_or_404(Socio, pk=pk)
    socio.delete()
    return redirect('lista_socios')

def editar_dependente(request, pk):
    dependente = get_object_or_404(Dependentes, pk=pk)
    dois_meses = timedelta(days=60) #validade do exame medico
    if request.method == 'POST':
        form = DependenteForm(request.POST, instance=dependente)
        if form.is_valid():
           #valida conforme filiação
            if dependente.filiacao == "FILHO(a)":
                qtd_anos = timedelta(days=365 * 25)
                #dependente.validade = timezone.now().date() + qtd_anos
                dependente.validade = dependente.data_nascimento + qtd_anos
            elif dependente.filiacao == "NETO(a)":
                qtd_anos = timedelta(days=365 * 12)
                #dependente.validade = timezone.now().date() + qtd_anos
                dependente.validade = dependente.data_nascimento + qtd_anos            
            dependente.dtexame_fin = timezone.now().date() + dois_meses
            form.save()
            return redirect('lista_dependentes')  # Redirecionar para página de sucesso após edição
    else:
        form = DependenteForm(instance=dependente)
    return render(request, 'editar_dependente.html', {'form': form})