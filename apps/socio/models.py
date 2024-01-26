# socios/models.py 
from django.db import models

class Socio(models.Model):

    OPC_CATEGORIA = [
        ("II", "Servidor Publico"),
        ("VI", "Particular")

    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20, null=True)
    
    tpsocio = models.CharField(
        verbose_name="Tipo de Socio",
        max_length=50,
        choices=OPC_CATEGORIA,
        default="ESPOSA(o)"
    )

    dtexame_ini = models.DateField(
        verbose_name="Dia do Exame",
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,

    )
    dtexame_fin = models.DateField(
        verbose_name="Validade do Exame",
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,

    )

    foto = models.ImageField(upload_to='static/images/', null=True, blank=True)
    nrcart = models.CharField(max_length=20, null=True)
    class Meta:
            verbose_name = "Sócio"
            verbose_name_plural = "Sócios"
            db_table = "socio"

    def __str__(self):
        return self.nome

class Dependentes(models.Model):
    OPC_FILIACAO = [
        ("ESPOSA(o)", "Esposa(o)"),
        ("FILHO(a)", "Filho(a)"),
        ("NETO(a)", "Neto(a)")
    ]

    socio = models.ForeignKey(Socio, on_delete=models.CASCADE,related_name='dependentes')
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    
    filiacao = models.CharField(
        verbose_name="Filiacao",
        max_length=50,
        choices=OPC_FILIACAO,
        default="ESPOSA(o)"
    )

    validade = models.DateField(
        verbose_name="Validade da Filiacao",
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,

    )

    dtexame_ini = models.DateField(
        verbose_name="Dia do Exame",
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,

    )
    dtexame_fin = models.DateField(
        verbose_name="Validade do Exame",
        auto_now_add=False,
        auto_now=False,
        blank=True,
        null=True,

    )

    foto = models.ImageField(upload_to='static/images/', null=True, blank=True)
    nrcart = models.CharField(max_length=20, null=True)

    class Meta:
            verbose_name = "Dependente"
            verbose_name_plural = "Dependentes"
            db_table = "dependentes"


    def __str__(self):
        return self.nome
