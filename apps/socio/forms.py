# socios/forms.py
from django import forms
from .models import Socio, Dependentes


class SocioForm(forms.ModelForm):
    
    class Meta:
        model = Socio
        fields = ['nome', 'email','cpf', 'data_nascimento', 'telefone', 'tpsocio', 'registro','cep','logradouro','cidade','estado' ,'dtexame_ini', 'dtexame_fin', 'foto']
        OPCOES = [('II', 'Servidor Publico'), ('VI', 'Particular')]
        tpsocio = forms.ChoiceField(choices=OPCOES)
        registro = forms.CharField(required=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['dtexame_fin'].widget.attrs['disabled'] = True
        #self.fields['registro'].widget.attrs['disabled'] = True
 
class DependenteForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'})
    )
    dtexame_ini = forms.DateField(
        required=False,  # Permitir que o campo fique em branco
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY'})
    )
    dtexame_fin = forms.DateField(
        required=False,  # Permitir que o campo fique em branco
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY', 'disabled': True})
    )
    validade = forms.DateField(
        required=False,  # Permitir que o campo fique em branco
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'class': 'form-control', 'placeholder': 'DD/MM/YYYY', 'disabled': True})
    )

    class Meta:
        model = Dependentes
        fields = ['nome', 'cpf', 'data_nascimento', 'filiacao', 'validade', 'dtexame_ini', 'dtexame_fin', 'foto', 'tpsocio']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['validade'].widget.attrs['disabled'] = True
        self.fields['dtexame_fin'].widget.attrs['disabled'] = True

class BuscaSocioForm(forms.Form):
    #socio_id = forms.IntegerField(label='Digite o RM do sócio')
    nrcart = forms.CharField(max_length=20, required=False, label='Número da Carterinha')    

class SocioSearchForm(forms.Form):
    #search_query = forms.CharField(max_length=20, required=False, label='Número da Carterinha')    
    search_term = forms.CharField(max_length=100, required=False, label='Buscar sócio')

class DependenteSearchForm(forms.Form):
    #search_query = forms.CharField(max_length=20, required=False, label='Número da Carterinha')    
    search_term = forms.CharField(max_length=100, required=False, label='Buscar dependente')