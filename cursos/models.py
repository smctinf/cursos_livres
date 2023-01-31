import random
from django.db import models
from django.contrib.auth.models import User


class Instituicao(models.Model):

    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return '%s' % (self.nome)


class Local(models.Model):

    nome = models.CharField(max_length=150, verbose_name='Nome do local')
    endereco = models.CharField(max_length=150, verbose_name='Endereço')
    bairro = models.CharField(max_length=80, verbose_name='Bairro')
    cep = models.CharField(max_length=9, verbose_name='CEP')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return '%s' % (self.nome)


class Categoria(models.Model):

    nome = models.CharField(max_length=150, verbose_name='Nome da categoria')

    def __str__(self):
        return '%s' % (self.nome)


class Curso(models.Model):

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    sigla = models.CharField(max_length=3, unique=True)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    carga_horaria = models.IntegerField(verbose_name="Carga horária")
    descricao = models.TextField(default='')
    ativo = models.BooleanField(default=True)

    dt_inclusao = models.DateField(auto_now_add=True, editable=False)
    dt_alteracao = models.DateField(auto_now=True)

    user_inclusao = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='userInclusao')
    user_ultima_alteracao = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='userAlteracao', null=True, blank=True)

    def __str__(self):
        return '%s' % (self.nome)


class Instrutor(models.Model):
    class Meta:
        verbose_name = 'Instrutor'
        verbose_name_plural = "Instrutores"

    nome = models.CharField(
        max_length=150, verbose_name='Nome completo do Instrutor')
    celular = models.CharField(max_length=15, verbose_name='Celular')
    email = models.EmailField(verbose_name='Email', blank=True)
    endereco = models.CharField(
        max_length=150, blank=True, null=True, verbose_name='Endereço')
    bairro = models.CharField(max_length=80, blank=True, null=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    dt_inclusao = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.nome)


class Turno(models.Model):

    def __str__(self):
        return '%s, de %s às %s' % (self.get_dia_semana_display(), self.horario_inicio, self.horario_fim)

    DIAS_SEMANA_CHOICES = (
        ('1', 'Domingo'),
        ('2', 'Segunda-Feira'),
        ('3', 'Terça-Feira'),
        ('4', 'Quarta-Feira'),
        ('5', 'Quinta-Feira'),
        ('6', 'Sexta-Feira'),
        ('7', 'Sábado'),
    )

    dia_semana = models.CharField(max_length=1, choices=DIAS_SEMANA_CHOICES)

    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()


class Turma(models.Model):

    STATUS_CHOICES = (
        ('pre', 'Pré-inscrição'),
        ('agu', 'Aguardando'),
        ('ati', 'Ativa'),
        ('acc', 'Ativa e aceitando candidatos'),
        ('enc', 'Encerrada'),
    )

    curso = models.ForeignKey(
        Curso, on_delete=models.CASCADE, verbose_name='Atividade')
    local = models.ForeignKey(Local, on_delete=models.CASCADE)

    instrutores = models.ManyToManyField(
        Instrutor, verbose_name='Instrutor(es)')
    quantidade_permitido = models.IntegerField(
        verbose_name='Quantidade de alunos permitidos')
    idade_minima = models.IntegerField(
        verbose_name='Idade mínima', null=True, blank=True)
    idade_maxima = models.IntegerField(
        verbose_name='Idade máxima', null=True, blank=True)

    data_inicio = models.DateField()
    data_final = models.DateField()

    turnos = models.ManyToManyField(Turno)

    dt_inclusao = models.DateField(auto_now_add=True, editable=False)
    dt_alteracao = models.DateField(auto_now=True)

    user_inclusao = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='TurmaUserInclusao')
    user_ultima_alteracao = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='TurmaUserAlteracao', null=True, blank=True)

    status = models.CharField(max_length=3, default='pre',
                              choices=STATUS_CHOICES, verbose_name='Qual o status da turma?')
    grupo_whatsapp = models.URLField(
        blank=True, null=True, verbose_name='Link do grupo do Whatsapp')

    def __str__(self):
        return '%s %s - %s' % (self.curso.nome, self.id, self.local)


class Aluno(models.Model):

    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Prefiro não informar')
    )

    ESCOLARIDADE_CHOICES = (
        ('efi', 'Ensino Fundamental Incompleto'),
        ('efc', 'Ensino Fundamental Completo'),
        ('emi', 'Ensino Médio Incompleto'),
        ('emc', 'Ensino Médio Completo'),
        ('ct', 'Curso Técnico'),
        ('esi', 'Ensino Superior Incompleto'),
        ('esc', 'Ensino Superior Completo'),
    )

    ESTADOCIVIL_CHOICES = (
        ('s', 'Solteiro(a)'),
        ('c', 'Casado(a)'),
        ('s', 'Separado(a)'),
        ('d', 'Divorciado(a)'),
        ('v', 'Viúvo(a)'),
    )

    nome = models.CharField(
        max_length=150, verbose_name='Nome completo do candidato')
    celular = models.CharField(
        max_length=15, verbose_name='Celular p/ contato do candidato')
    email = models.EmailField(verbose_name='Email p/ contato do candidato')
    dt_nascimento = models.DateField(verbose_name='Data de Nascimento')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES,
                            verbose_name='Qual foi o sexo atribuído no seu nascimento?')
    cep = models.CharField(max_length=9, verbose_name='CEP')
    endereco = models.CharField(
        max_length=128, null=True, verbose_name='Endereço do candidato')

    complemento = models.CharField(
        max_length=128, null=True, blank=True, verbose_name='Complemento do endereço')

    bairro = models.CharField(max_length=80, null=True)
    cpf = models.CharField(max_length=150, verbose_name='CPF')
    profissão = models.CharField(max_length=150, verbose_name='Profissão')
    escolaridade = models.CharField(
        max_length=3, choices=ESCOLARIDADE_CHOICES, verbose_name='Escolaridade')
    estado_civil = models.CharField(
        max_length=1, choices=ESTADOCIVIL_CHOICES, verbose_name='Estado Civil')
    aceita_mais_informacoes = models.BooleanField(
        verbose_name='Declaro que aceito receber email com as informações das atividades')
    li_e_aceito_termos = models.BooleanField(
        default=False, verbose_name='Li e aceito os termos')

    dt_inclusao = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s' % (self.nome)


class Responsavel(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    ESTADOCIVIL_CHOICES = (
        ('s', 'Solteiro(a)'),
        ('c', 'Casado(a)'),
        ('s', 'Separado(a)'),
        ('d', 'Divorciado(a)'),
        ('v', 'Viúvo(a)'),
    )
    nome = models.CharField(
        max_length=150, verbose_name='Nome completo do responsável')
    celular = models.CharField(
        max_length=15, verbose_name='Celular p/ contato do responsável')
    email = models.EmailField(verbose_name='Email p/ contato do responsável')
    dt_nascimento = models.DateField(verbose_name='Data de Nascimento')
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES,
                            verbose_name='Qual foi o sexo atribuído no seu nascimento?')
    cep = models.CharField(max_length=9, verbose_name='CEP')
    endereco = models.CharField(
        max_length=150, null=True, verbose_name='Endereço do responsável')
    bairro = models.CharField(
        verbose_name='Bairro', max_length=80, null=True)
    cpf = models.CharField(max_length=14, verbose_name='CPF')
    profissao = models.CharField(max_length=150, verbose_name='Profissão')
    estado_civil = models.CharField(
        max_length=1, choices=ESTADOCIVIL_CHOICES, verbose_name='Estado Civil')
    aluno = models.ForeignKey(
        Aluno, on_delete=models.CASCADE, blank=True, null=True)
    dt_inclusao = models.DateField(auto_now_add=True)


class Matricula(models.Model):
    STATUS_CHOICES = (
        ('c', 'Candidato'),
        ('s', 'Selecionado'),
        ('a', 'Aluno'),
        ('d', 'Aluno desistente'),
    )

    def save(self, *args, **kwargs):

        turma_id = str(self.turma.id)
        aluno_id = str(self.aluno.id)
        instituicao = str(self.turma.curso.instituicao.sigla).upper()
        curso = str(self.turma.curso.sigla).upper()

        total_length = len(turma_id) + len(aluno_id) + len(instituicao) + len(curso)

        if total_length > 16:
            raise ValueError(
                "The total length of turma_id, aluno_id and instituicao must be less than or equal to 16")
        
        self.matricula = instituicao + curso + turma_id.rjust(16 - total_length + len(turma_id), "0")  + aluno_id 
        print(self)
        super().save(*args, **kwargs)

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    matricula = models.CharField(
        max_length=16, unique=True, editable=False, primary_key=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    dt_inclusao = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return '%s - %s' % (self.turma, self.aluno)
