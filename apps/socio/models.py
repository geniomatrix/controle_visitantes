# socios/models.py 
from django.db import models

class Socio(models.Model):

    OPC_CATEGORIA = [
        ("II", "Servidor Publico"),
        ("VI", "Particular")

    ]

    OPC_ATIVAR = [
        ("S", "Sim"),
        ("N", "Nao")

    ]

    nome = models.CharField(max_length=100)
    #email = models.EmailField(unique=True)
    email = models.EmailField(unique=False,max_length=40, null=True,blank=True,)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20, null=True)

    ativo = models.CharField(
        verbose_name="Ativar Socio",
        max_length=10,
        choices=OPC_ATIVAR,
        default="Sim"
    )

    
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
    #foto = models.ImageField(upload_to='images', null=True, blank=True)
    nrcart = models.CharField(max_length=20, null=True)
    registro = models.CharField(verbose_name="Numero da Matricula no caso de servidor publico",max_length=20, null=True,blank=True)
    cpf = models.CharField(max_length=20, null=True, blank=True)
    
    #endereço
    logradouro = models.CharField(verbose_name="AV/Rua",max_length=255, null=True,blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True)
    cep = models.CharField(max_length=9, null=True, blank=True)

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
        ("NETO(a)", "Neto(a)"),
        ("BISNETO(a)", "Bisneto(a)"),
        ("SOGRO(a)", "Sogro(a)"),
        ("PAIS", "Pais"),
    ]

    OPC_ATIVAR = [
            ("S", "Sim"),
            ("N", "Nao")

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
    
    cpf = models.CharField(max_length=20, null=True, blank=True)
    ativo = models.CharField(
        verbose_name="Ativar Socio",
        max_length=10,
        choices=OPC_ATIVAR,
        default="Sim"
    )
    tpsocio = models.CharField(
        verbose_name="Tipo de Socio",
        max_length=20,
        null=True,
        blank=True
    )

    class Meta:
            verbose_name = "Dependente"
            verbose_name_plural = "Dependentes"
            db_table = "dependentes"


    def __str__(self):
        return self.nome
