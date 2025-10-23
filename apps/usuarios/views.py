from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model,login

from django import forms
from django.contrib.auth import get_user_model  # Importa get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from usuarios.forms import PasswordResetLocalForm

from .forms import PasswordResetLocalForm  # ajuste o import conforme seu projeto

# Obter o modelo de usuário personalizado
User = get_user_model()

# Formulário de registro personalizado
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

Usuario = get_user_model()

def password_reset_local(request):
    if request.method == 'POST':
        form = PasswordResetLocalForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            nova_senha = form.cleaned_data['nova_senha']
            try:
                user = User.objects.get(email=email)
                user.set_password(nova_senha)
                user.save()
                messages.success(request, "Senha redefinida com sucesso! Faça login com sua nova senha.")
                return redirect('login')  # redireciona para limpar tudo
            except User.DoesNotExist:
                messages.error(request, "Usuário com este e-mail não encontrado.")
                # cairá no render abaixo; form já tem erros de mensagens
        # Se inválido (ou usuário não existe), antes de renderizar forçamos limpar os campos de senha no widget
        # (apenas para garantir que nenhum valor seja mostrado)
        form.fields['nova_senha'].widget.attrs.pop('value', None)
        form.fields['confirmar_senha'].widget.attrs.pop('value', None)
    else:
        form = PasswordResetLocalForm()

    return render(request, 'password_reset_local.html', {'form': form})

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ['nome','email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está sendo utilizado.")
        return email


# View de registro usando o formulário personalizado
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro realizado com sucesso!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# View de login personalizada com mensagens de feedback
class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, "Login realizado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Erro ao logar. Verifique suas credenciais.")
        return super().form_invalid(form)
    
