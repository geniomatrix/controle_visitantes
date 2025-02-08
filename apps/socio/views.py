# socios/views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from .models import Socio, Dependentes
from .forms import SocioForm, DependenteForm,BuscaSocioForm,SocioSearchForm,DependenteSearchForm
from datetime import date, timedelta,datetime
from django.utils import timezone
from .utils import preencher_endereco_por_cep
import qrcode
from io import BytesIO
from django.core.files import File
import base64
from django.http import HttpResponseRedirect,JsonResponse
import cv2
import numpy as np
from dateutil.relativedelta import relativedelta
from django.db.models import Q  # Importa Q para a query com OR
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now


def is_porteiro(user):
    return user.groups.filter(name="Porteiros").exists()

def gerar_qr_code(data):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=2)
    qr.add_data(data)
    #redimensiona o conteúdo do qrcode para caber o conteúdo
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
 
    buffer = BytesIO()
    img.save(buffer)
    return buffer.getvalue()


def carteirinha(request, pk):
    #socio = get_object_or_404(Socio, pk=socio_id)
    socio = Socio.objects.get(pk=pk)
    if socio.nome and socio.nrcart:
        #qr_code_data = f"Nome: {socio.nome}, Número do Sócio: {socio.nrcart}"
        qr_code_data = f"{socio.nrcart}"
        qr_code_bytes = gerar_qr_code(qr_code_data)
        qr_code_base64 = base64.b64encode(qr_code_bytes).decode('utf-8')
        return render(request, 'carteirinha.html', {'socio': socio, 'qr_code_base64': qr_code_base64})
    else:
        # Se algum dos campos estiver vazio, retorne uma resposta de erro ou faça o tratamento adequado
        return render(request, 'erro.html', {'mensagem': 'Os dados do sócio estão incompletos'})


def cartdep(request, pk):
    
    dependentes = Dependentes.objects.get(pk=pk)
    
    if dependentes.nome and dependentes.nrcart:
        socio_id = dependentes.socio.id
        socio = Socio.objects.get(pk=socio_id)
        qr_code_data = f"{dependentes.nrcart}"
        qr_code_bytes = gerar_qr_code(qr_code_data)
        qr_code_base64 = base64.b64encode(qr_code_bytes).decode('utf-8')
        return render(request, 'carteirinhadep.html', {'dependentes': dependentes, 'qr_code_base64': qr_code_base64,'socio': socio})
    else:
        # Se algum dos campos estiver vazio, retorne uma resposta de erro ou faça o tratamento adequado
        return render(request, 'erro.html', {'mensagem': 'Os dados do dependente estão incompletos'})


def lista_socioscart(request):
    
    socios = Socio.objects.all()
    dependentes = Dependentes.objects.all()
    query = request.GET.get('q')
    if query:
        socios = socios.filter(nome__icontains=query)
        dependentes = dependentes.filter(nome__icontains=query)
        paginator = Paginator(socios, 10)  # Exibir 10 sócios por página
        
        page = request.GET.get('page')

    
        try:
            socios = paginator.get_page(page)
        except PageNotAnInteger:
            # Se page não for um inteiro, exibir a primeira página
            socios = paginator.get_page(1)
        except EmptyPage:
            # Se a página está fora do intervalo, exibir a última página de resultados
            socios = paginator.get_page(paginator.page)
    
    
    context = {'socios': socios, 'dependentes': dependentes}
    
    return render(request, 'lista_socioscart.html', context)
 
    

@login_required
def lista_socios(request):
    
    #socio = Socio.objects.all() #Socio.objects.filter(ativo='Sim')
    #return render(request, 'lista_socios.html', {'socio': socio})
    form = SocioSearchForm(request.GET)
    socios = Socio.objects.all()

    if form.is_valid():
        search_term = form.cleaned_data['search_term']
        socios = socios.filter(nome__icontains=search_term)
        paginator = Paginator(socios, 30)  # Exibir 10 sócios por página
        page = request.GET.get('page')
        try:
            socios = paginator.page(page)
        except PageNotAnInteger:
            # Se page não for um inteiro, exibir a primeira página
            socios = paginator.page(1)
        except EmptyPage:
            # Se a página está fora do intervalo, exibir a última página de resultados
            socios = paginator.page(paginator.num_pages)

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
        paginator = Paginator(socios, 30)  # Exibir 10 sócios por página
        page = request.GET.get('page')
        try:
            socios = paginator.page(page)
        except PageNotAnInteger:
            # Se page não for um inteiro, exibir a primeira página
            socios = paginator.page(1)
        except EmptyPage:
            # Se a página está fora do intervalo, exibir a última página de resultados
            socios = paginator.page(paginator.num_pages)

    context = {'socio': socios, 'form': form}
    return render(request, 'lista_socios_altera.html', context)


def lista_dependentes(request):
    
    form = DependenteSearchForm(request.GET)
    dependentes = Dependentes.objects.all().order_by('nome')

    if form.is_valid():
        search_term = form.cleaned_data['search_term']
        #socios = socios.filter(nome__icontains=search_term) | socios.filter(registro__icontains=search_term)
        dependentes = dependentes.filter(nome__icontains=search_term)
        paginator = Paginator(dependentes, 30)  # Exibir 10 sócios por página
        page = request.GET.get('page')
        try:
            dependentes = paginator.page(page)
        except PageNotAnInteger:
            # Se page não for um inteiro, exibir a primeira página
            dependentes = paginator.page(1)
        except EmptyPage:
            # Se a página está fora do intervalo, exibir a última página de resultados
            dependentes = paginator.page(paginator.num_pages)

    context = {'dependentes': dependentes, 'form': form}
    return render(request, 'lista_dependentes.html', context)

def lista_dependentes_altera(request):
    
    form = DependenteSearchForm(request.GET)
    dependentes = Dependentes.objects.all()

    if form.is_valid():
        search_term = form.cleaned_data['search_term']
        #socios = socios.filter(nome__icontains=search_term) | socios.filter(registro__icontains=search_term)
        dependentes = dependentes.filter(nome__icontains=search_term)
        paginator = Paginator(dependentes, 30)  # Exibir 10 sócios por página
        page = request.GET.get('page')
        try:
            dependentes = paginator.page(page)
        except PageNotAnInteger:
            # Se page não for um inteiro, exibir a primeira página
            dependentes = paginator.page(1)
        except EmptyPage:
            # Se a página está fora do intervalo, exibir a última página de resultados
            dependentes = paginator.page(paginator.num_pages)


    context = {'dependentes': dependentes, 'form': form}
    return render(request, 'lista_dependentes_altera.html', context)

def detalhes_socio(request, socio_id):
    socio = get_object_or_404(Socio, pk=socio_id)
    data_atual = date.today()
    dois_meses = timedelta(days=60)
    diferenca_dias = None  # Inicializando a variável
    dependente_form = DependenteForm()

    if request.method == 'POST':
        dependente_form = DependenteForm(request.POST, request.FILES)
        if dependente_form.is_valid():
            dependente = dependente_form.save(commit=False)
            dependente.socio = socio

            # Validação conforme filiação
            idade = relativedelta(data_atual, dependente.data_nascimento).years
            if dependente.filiacao == "FILHO(a)" and idade > 22:
                messages.error(request, "Dependente do tipo FILHO(a) deve ter até 22 anos.")
                return redirect('detalhes_socio', socio_id=socio_id)
            elif (dependente.filiacao == "NETO(a)" or dependente.filiacao == "BISNETO(a)")  and idade > 13:
                messages.error(request, "Dependente do tipo NETO(a) ou BISNETO(a) deve ter até 13 anos.")
                return redirect('detalhes_socio', socio_id=socio_id)

            # Define validade
            if dependente.filiacao == "FILHO(a)":
                dependente.validade = dependente.data_nascimento + relativedelta(years=22) - timedelta(days=1)
            elif dependente.filiacao == "NETO(a)" or dependente.filiacao == "BISNETO(a)":
                dependente.validade = dependente.data_nascimento + relativedelta(years=13) - timedelta(days=1)

            # Ajusta data de exame
            
            if dependente.dtexame_ini and dependente.dtexame_fin:
                diferenca_dias = (dependente.dtexame_fin - dependente.dtexame_ini).days
            elif dependente.dtexame_ini:
                # Caso `dtexame_fin` não exista, define como `dtexame_ini + dois_meses`
                dependente.dtexame_fin = dependente.dtexame_ini + dois_meses

            # Gera número do cartão
            ultimo_registro = Dependentes.objects.last()
            proximo_id = (ultimo_registro.id + 1) if ultimo_registro else 1
            dependente.nrcart = f"D{proximo_id}{socio_id}{socio.tpsocio}"

            try:
                dependente.save()
                messages.success(request, "Dependente registrado com sucesso!")
            except Exception as e:
                messages.error(request, f"Erro ao salvar o dependente: {str(e)}")
                return redirect('detalhes_socio', socio_id=socio_id)

            return redirect('detalhes_socio', socio_id=socio_id)

    return render(request, 'detalhes_socio.html', {
        'socio': socio,
        'dependente_form': dependente_form,
        'data_atual': data_atual,


    })

def detalhes_dependente(request, dependente_id):
    # Obter o dependente pelo ID
    dependente = get_object_or_404(Dependente, pk=dependente_id)
    dependente_form = DependenteForm()
    
    dois_meses = timedelta(days=60)  # Validade do exame médico
    diferenca_maior_que_60 = False  # Variável para armazenar o estado da diferença

    if dependente.dtexame_ini and dependente.dtexame_fin:
        # Calcular a diferença entre as datas
        diferenca_dias = (dependente.dtexame_fin - dependente.dtexame_ini).days
        diferenca_maior_que_60 = diferenca_dias > 60

    if request.method == 'POST':
        dependente_form = DependenteForm(request.POST)
        if dependente_form.is_valid():
            dependente = dependente_form.save(commit=False)

            # Validação conforme a filiação
            if dependente.filiacao == "FILHO(a)":
                dependente.validade = dependente.data_nascimento + relativedelta(years=26) - timedelta(days=1)
            elif dependente.filiacao == "NETO(a)" or dependente.filiacao == "BISNETO(a)":
                dependente.validade = dependente.data_nascimento + relativedelta(years=13) - timedelta(days=1)

            # Atualizar a validade do exame médico
            dependente.dtexame_fin = timezone.now().date() + dois_meses

            # Gerar o número do cartão
            existe_registros = Dependente.objects.exists()
            if existe_registros:
                ultimo_registro = Dependente.objects.latest('id')
                proximo_registro = ultimo_registro.id + 1
            else:
                proximo_registro = 1

            dependente.nrcart = f"D{proximo_registro}{socio_id}{socio.tpsocio}"
            dependente.save()
            return redirect('detalhes_dependente', dependente_id=dependente.id)

    return render(request, 'detalhes_dependente.html', {
        'dependente': dependente,
        'dependente_form': dependente_form,
        'diferenca_maior_que_60': diferenca_maior_que_60,
    })


def buscar_socio(request):
    
    socio_id = None
    data_atual = date.today()  # Data atual
    if request.method == 'POST':
        form = BuscaSocioForm(request.POST)
        if form.is_valid():
            #socio_id = form.cleaned_data['socio_id']
            nrcart = form.cleaned_data['nrcart']
            
            try:
                #socio = Socio.objects.get(pk=socio_id)
                socio = Socio.objects.get(nrcart=nrcart)
                socio_id = socio.id
                #verifica se o sócio esta ativo
                socio_ativo = verificar_socio_ativo(socio_id)
                if socio_ativo != 'N':
                    return render(request, 'detalhes_sociocart.html', {'socio': socio, 'socio_id': socio_id, 'data_atual': data_atual})
                else:
                    return render(request, 'detalhes_sociocart_inativo.html', {'socio': socio, 'socio_id': socio_id, 'data_atual': data_atual})    
                #return redirect('detalhes_socio', socio_id=socio_id)
            except Socio.DoesNotExist:
                try:
                    dependente = Dependentes.objects.get(nrcart=nrcart)
                    socio = dependente.socio
                    dependente_id = dependente.id
                    dependente_ativo = verificar_dependente_ativo(dependente_id)
                    if dependente_ativo != 'N':
                        return render(request, 'detalhes_dependente.html', {'dependente': dependente, 'socio': socio, 'socio_id': socio_id,'data_atual': data_atual})
                    else:
                        return render(request, 'detalhes_dependente_inativo.html', {'dependente': dependente, 'socio': socio, 'socio_id': socio_id,'data_atual': data_atual})    

                except Dependentes.DoesNotExist:
                    mensagem = 'Sócio e dependente não encontrado.'.format(nrcart)
                    return render(request, 'registrone.html', {'mensagem': mensagem, 'form': form})
    else:
        form = BuscaSocioForm()

    return render(request, 'buscar_socio_acesso.html', {'form': form, 'data_atual': data_atual})

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
            messages.success(request, "Sócio registrado com sucesso!")
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
                #dois_meses = timedelta(days=60)
                #form.instance.dtexame_fin = timezone.now().date() + dois_meses
                form.instance.nrcart = "S" + str(proximo_registro) + form.instance.tpsocio
                #form.instance.foto = form.instance.foto.FILES['foto']
                form.save()
            else:
                #dois_meses = timedelta(days=60)
                #form.instance.dtexame_fin = timezone.now().date() + dois_meses
                form.instance.nrcart = "S" + str(1) + form.instance.tpsocio
                #form.instance.foto = form.instance.foto.FILES['foto']
                form.save()
                
            return redirect('lista_socios')
    else:
        form = SocioForm()
    return render(request, 'cadastrar_socio.html', {'form': form})

def editar_socio(request, pk):
    
    socio = get_object_or_404(Socio, pk=pk)
    if request.method == 'POST':
        form = SocioForm(request.POST, request.FILES, instance=socio)  # Adicionando request.FILES
        dois_meses = timedelta(days=60)  #validade do exame medico
        if form.is_valid():
            if socio.dtexame_ini:
                if socio.dtexame_fin:
                    diferenca_dias = socio.dtexame_ini - socio.dtexame_fin
                    if diferenca_dias.days > 60:
                        socio.dtexame_fin = socio.dtexame_ini + dois_meses
                else:
                    socio.dtexame_fin = socio.dtexame_ini + dois_meses            
            form.save()
            messages.success(request, "Sócio alterado com sucesso!")
            return redirect('lista_socios_altera')
    else:
        form = SocioForm(instance=socio)
    return render(request, 'editar_socio.html', {'form': form})

def excluir_socio(request, pk):
    socio = get_object_or_404(Socio, pk=pk)
    socio.delete()
    messages.success(request, "Socio excluído com sucesso!")
    return redirect('lista_socios')

def editar_dependente(request, pk):
    
    dependente = get_object_or_404(Dependentes, pk=pk)
    dois_meses = timedelta(days=60) #validade do exame medico
    if request.method == 'POST':
        form = DependenteForm(request.POST, request.FILES,instance=dependente)
        
        if form.is_valid():
           
           #valida conforme filiação
            
            if dependente.filiacao == "FILHO(a)":
                #qtd_anos = timedelta(days=365 * 26) - timedelta(days=1)
                #dependente.validade = timezone.now().date() + qtd_anos
                dependente.validade = dependente.data_nascimento + relativedelta(years=26) - timedelta(days=1)
            elif dependente.filiacao == "NETO(a)" or dependente.filiacao == "BISNETO(a)":
                #qtd_anos = timedelta(days=365 * 13) - - timedelta(days=1)
                #dependente.validade = timezone.now().date() + qtd_anos
                dependente.validade = dependente.data_nascimento + relativedelta(years=13) - timedelta(days=1)            
            #dependente.dtexame_fin = timezone.now().date() + dois_meses
            if dependente.dtexame_ini:
                if dependente.dtexame_fin:
                    diferenca_dias = dependente.dtexame_ini - dependente.dtexame_fin
                    if diferenca_dias.days > 60:
                        dependente.dtexame_fin = dependente.dtexame_ini + dois_meses
                    else:
                        dependente.dtexame_fin = dependente.dtexame_ini + dois_meses            
                else:
                    dependente.dtexame_fin = dependente.dtexame_ini + dois_meses
            form.save()
            messages.success(request, "Dependente alterado com sucesso!")
            return redirect('lista_dependentes')  # Redirecionar para página de sucesso após edição
    else:
        form = DependenteForm(instance=dependente)
    return render(request, 'editar_dependente.html', {'form': form})

def excluir_dependente(request, pk):
    dependente = get_object_or_404(Dependentes, pk=pk)
    dependente.delete()
    messages.success(request, "Dependente excluído com sucesso!")
    return redirect('lista_socios')

def editar_socio_foto(request, pk):
    
    socio = get_object_or_404(Socio, pk=pk)

    if request.method == 'POST':
        socio.nome = request.POST['nome']
        # Se uma nova foto foi tirada, atualiza a foto do sócio
        if 'foto_base64' in request.POST:
            socio.foto = foto_base64_to_image(request.POST['foto_base64'])
        socio.save()
        #return HttpResponseRedirect('sucesso')  # Redirecionar para uma página de sucesso

    return render(request, 'editar_socio_foto.html', {'socio': socio})

def foto_base64_to_image(foto_base64):
    import base64
    from django.core.files.base import ContentFile
    import io
    from PIL import Image

    foto_decoded = base64.b64decode(foto_base64.split(",")[1])
    image_content = ContentFile(foto_decoded)
    return image_content
    
def capturar_foto(request):
    try:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            raise IOError("Não foi possível abrir a câmera.")

        ret, frame = cap.read()
        cap.release()

        if not ret:
            raise IOError("Erro ao capturar imagem da câmera.")

        # Definindo o caminho onde a imagem será salva
        caminho_imagem = 'static/images/captura.jpg'

        # Salvando a imagem capturada
        cv2.imwrite(caminho_imagem, frame)

        # Retornando o caminho da imagem salva para o cliente
        return JsonResponse({'url': caminho_imagem})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def upload_photo(request):
    if request.method == 'POST' and request.FILES['foto']:
        foto = request.FILES['foto']
        # Aqui você pode salvar a imagem como desejar
        # Exemplo de salvar no banco de dados:
        novo_socio = Socio(foto=foto)
        novo_socio.save()
        return JsonResponse({'message': 'Foto recebida e salva com sucesso!'})
    else:
        return JsonResponse({'error': 'Nenhuma imagem recebida.'}, status=400)

def verificar_socio_ativo(socio_id):
    try:
        socio = Socio.objects.get(id=socio_id)
        return socio.ativo == 'S'
    except Socio.DoesNotExist:
        return False

def verificar_dependente_ativo(socio_id):
    try:
        dependentes = Dependentes.objects.get(id=socio_id)
        return dependentes.ativo == 'S'
    except Dependentes.DoesNotExist:
        return False
    


def pagar_taxasocio(request, pk):
    # Obtenha o socio pelo ID
    socio = get_object_or_404(Socio, pk=pk)
    
    # Atualize os campos de data
    socio.dtexame_ini = now()  # Data atual
    socio.dtexame_fin = now() + timedelta(days=60)  # Adiciona 2 meses
    socio.save()

    # Mensagem de confirmação
    messages.success(request, f"A taxa de piscina para {socio.nome} foi paga com sucesso!")
    
    # Redirecione para a página de detalhes do socio
    return redirect('buscar_socio')
  
def pagar_taxadep(request, pk):
    # Obtenha o dependente pelo ID
    dependente = get_object_or_404(Dependentes, pk=pk)
    
    # Atualize os campos de data
    dependente.dtexame_ini = now()  # Data atual
    dependente.dtexame_fin = now() + timedelta(days=60)  # Adiciona 2 meses
    dependente.save()

    # Mensagem de confirmação
    messages.success(request, f"A taxa de piscina para {dependente.nome} foi paga com sucesso!")
    
    # Redirecione para a página de detalhes do dependente
    return redirect('buscar_socio')
  
