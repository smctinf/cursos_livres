from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from autenticacao.functions import aluno_required
from .models import *
from .forms import *
from datetime import date, datetime

from .models import *
from .forms import *

from eventos.models import Evento


def index(request):
    context = {
        'titulo': 'Capacitação',
        'evento_destaque': Evento.objects.get(is_destaque = True)
    }

    return render(request, 'cursos/index.html', context)


@aluno_required
def cursos(request):
    form = Aluno_form()
    categorias = Categoria.objects.all()
    cursos = []
    for i in categorias:
        cursos.append(
            {'categoria': i, 'curso': Curso.objects.filter(categoria=i, ativo=True)})

    context = {
        'categorias': cursos,
        'form': form,
        'titulo': 'Capacitação'
    }
    return render(request, 'cursos/cursos.html', context)


@login_required
def candidatar(request, id):

    curso = Curso.objects.get(id=id)
    form = Aluno_form(initial={'curso': curso})
    if request.method == 'POST':
        form = Aluno_form(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
        'titulo': 'Capacitação'
    }
    return render(request, 'cursos/cadastrar_candidato.html', context)


def prematricula(request):
    form = Aluno_form(prefix="candidato")
    form_responsavel = CadastroResponsavelForm(prefix="responsavel")

    categorias = Categoria.objects.all()
    cursos = []

    for i in categorias:
        cursos.append(
            {'categoria': i, 'curso': Curso.objects.filter(categoria=i, ativo=True)})

    if request.method == 'POST':
        dtnascimento_cp = request.POST.get("candidato-dt_nascimento")
        form = Aluno_form(request.POST, prefix="candidato")
        form_responsavel = CadastroResponsavelForm(
            request.POST, prefix="responsavel")

        try:
            dtnascimento_hr = datetime.strptime(dtnascimento_cp, "%d-%m-%Y")
        except:
            dtnascimento_hr = datetime.strptime(dtnascimento_cp, "%Y-%m-%d")

        dt_nascimento = dtnascimento_hr.date()

        today = date.today()
        age = today.year - dt_nascimento.year - \
            ((today.month, today.day) < (dt_nascimento.month, dt_nascimento.day))
        teste = True
        candidato = ""

        try:
            cpf = request.POST['cpf']
            candidato = Aluno.objects.get(cpf=cpf)
        except Exception as e:
            pass

        for i in request.POST.getlist('turmas'):
            turma = Turma.objects.get(id=i)
            if candidato:
                try:
                    Matricula.objects.get(
                        candidato=candidato, turma__curso=turma.curso)
                    messages.error(
                        request, 'Candidato já matriculado no curso ' + turma.curso.nome)
                    return redirect('/prematricula')
                except:
                    pass

            if (turma.idade_minima is not None and age < turma.idade_minima) or (turma.idade_maxima is not None and age > turma.idade_maxima):
                teste = False

        if form.is_valid() and teste:
            candidato = form.save(commit=False)

            if age < 18:

                if form_responsavel.is_valid():

                    responsavel = form_responsavel.save(commit=False)
                    responsavel.aluno = candidato

                else:
                    return redirect('/prematricula')

                responsavel.save()
                candidato.save()

            else:

                candidato.save()

            for i in request.POST.getlist('turmas'):
                Matricula.objects.create(
                    aluno=candidato, turma=turma, status='c')

            messages.success(
                request, 'Pré-inscrição realizada com sucesso! Aguarde nosso contato para finalizar inscrição.')
            return redirect('/')
        else:
            if not teste:
                messages.error(
                    request, 'Não foi possível realizar a inscrição na turma: A idade não atende a faixa etária da turma.')
                return redirect('/prematricula')

    context = {
        'form': form,
        'form_responsavel': form_responsavel,
        'categorias': cursos,
        'titulo': 'Capacitação'
    }
    return render(request, 'cursos/pre_matricula.html', context)


def login_view(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if "next" in request.GET:
                return redirect(request.GET.get('next'))
            return redirect('/')
        else:
            context = {
                'error': True,
            }

    return render(request, 'registration/login.html', context)


def alterarCad(request):
    return render(request, 'cursos/alterar_cad.html')


def resultado(request):
    return render(request, 'cursos/resultado.html')
