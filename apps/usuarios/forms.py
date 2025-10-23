from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class PasswordResetLocalForm(forms.Form):
    email = forms.EmailField(
        label="E-mail",
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite seu e-mail',
                'id': 'id_email',
                'autocomplete': 'email'
            }
        )
    )
    nova_senha = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Digite a nova senha',
                'id': 'id_new_password',
                'autocomplete': 'new-password'
            },
            render_value=False  # importantíssimo: não reapresenta o valor
        )
    )
    confirmar_senha = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirme a nova senha',
                'id': 'id_confirm_password',
                'autocomplete': 'new-password'
            },
            render_value=False
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        senha1 = cleaned_data.get('nova_senha')
        senha2 = cleaned_data.get('confirmar_senha')

        if senha1 and senha2 and senha1 != senha2:
            raise forms.ValidationError("As senhas não coincidem.")

        email = cleaned_data.get('email')
        if email and not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Nenhum usuário encontrado com este e-mail.")

        return cleaned_data
