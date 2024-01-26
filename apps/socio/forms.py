# socios/forms.py
from django import forms
from .models import Socio, Dependentes


class SocioForm(forms.ModelForm):
    
    class Meta:
        model = Socio
        fields = ['nome', 'email', 'data_nascimento', 'telefone', 'tpsocio', 'dtexame_ini', 'dtexame_fin', 'foto']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dtexame_fin'].widget.attrs['disabled'] = True    

class DependenteForm(forms.ModelForm):
    class Meta:
        model = Dependentes
        fields = ['nome', 'data_nascimento','filiacao','validade','dtexame_ini','dtexame_fin','foto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['validade'].widget.attrs['disabled'] = True
        self.fields['dtexame_fin'].widget.attrs['disabled'] = True

class BuscaSocioForm(forms.Form):
    #socio_id = forms.IntegerField(label='Digite o RM do sócio')
    nrcart = forms.CharField(max_length=20, required=False, label='Número da Carterinha')    

class SocioSearchForm(forms.Form):
    search_query = forms.CharField(max_length=20, required=False, label='Número da Carterinha')    