from django import forms
from datetime import date

from visitantes.models import Visitante


class VisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = [
            "nome_completo","cpf", "data_nascimento","numero_casa"
             
        ]
  
        error_messages = {
            "nome_completo": {
                "required": "O nome completo do visitante é obrigatório para o registro"
            },
            "cpf": {
                "required": "O CPF do visitante é obrigatório para o registro"
            },
            "data_nascimento": {
                "required": "A data de nascimetno do visitante é obrigatório para o registro",
                "invalid": "Por favor, informe um formato válido para data de nascimento (DD/MM/AAAA)"
            },
            "numero_casa": {
                "required": "Por favor, informe o número do quisque a ser visitada"
            }
   
        }


   


class AutorizaVisitanteForm(forms.ModelForm):
    morador_responsavel = forms.CharField(required=True)

    class Meta:
        model = Visitante
        fields = [
            "morador_responsavel"
        ]
        error_messages = {
            "morador_responsavel": {
                "required": "Por favor, informe o nome do responsavel por autorizar a entrada do visitante"
            }
        }
        
class BuscaVisitanteForm(forms.Form):
    termo_busca = forms.CharField(max_length=100, required=False)