from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import ListaExercicios

# TODO Colocar Login Required depois que as features estiverem prontas

# --- PÁGINA DO ALUNO (SPA) ---
def home(request):
    """
    Página principal que contém toda a interface do aluno (Aulas, Materiais, Simulados)
    carregada dinamicamente via JavaScript.
    """
    return render(request, 'home.html')


# --- ÁREA DO PROFESSOR: BIOLOGIA ---
def admin_bio_painel(request):
    return render(request, 'admin/biologia/painel.html', {"active_page": "dashboard"})


def admin_bio_desempenho(request):
    # Usa o mesmo template SPA, iniciando na aba de desempenho
    return render(request, 'admin/biologia/painel.html', {"active_page": "desempenho"})


def admin_bio_ferramentas(request):
    # Usa o mesmo template SPA, iniciando na aba de ferramentas/atlas digital
    return render(request, 'admin/biologia/painel.html', {"active_page": "ferramentas"})


# --- ÁREA DO PROFESSOR: FÍSICA ---
def admin_fis_painel(request):
    return render(request, 'admin/fisica/painel.html', {"active_page": "dashboard"})


def admin_fis_desempenho(request):
    # Usa o mesmo template SPA, iniciando em desempenho
    return render(request, 'admin/fisica/painel.html', {"active_page": "desempenho"})


def admin_fis_ferramentas(request):
    # Usa o mesmo template SPA, iniciando em ferramentas
    return render(request, 'admin/fisica/painel.html', {"active_page": "ferramentas"})


# --- ÁREA DO PROFESSOR: MATEMÁTICA ---
def admin_mat_painel(request):
    return render(request, 'admin/matematica/painel.html', {"active_page": "dashboard"})


def admin_mat_desempenho(request):
    # Usa o mesmo template SPA, iniciando em desempenho
    return render(request, 'admin/matematica/painel.html', {"active_page": "desempenho"})


def admin_mat_ferramentas(request):
    # Usa o mesmo template SPA, iniciando em ferramentas
    return render(request, 'admin/matematica/painel.html', {"active_page": "ferramentas"})


# --- ÁREA DO PROFESSOR: OUTRAS MATÉRIAS ---
def admin_quim_painel(request):
    return render(request, 'admin/quimica/painel.html')


def admin_hist_painel(request):
    return render(request, 'admin/historia/painel.html')


def admin_geo_painel(request):
    return render(request, 'admin/geografia/painel.html')


def admin_port_painel(request):
    return render(request, 'admin/portugues/painel.html')

# Sistema de Upload de Listas
def upload_lista(request, materia):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        arquivo = request.FILES.get('arquivo')

        if not arquivo or not arquivo.name.lower().endswith('.pdf'):
            messages.error(request, 'Apenas PDFs são permitidos')
        else:
            ListaExercicios.objects.create(
                titulo=titulo,
                arquivo=arquivo,
                materia=materia,
                professor=request.user.username if request.user.is_authenticated else "anon"
            )
            messages.success(request, f'Upload de {materia} realizado com sucesso!')

        # Redirect por matéria
        if materia == 'biologia':
            return redirect('admin_bio_painel')
        if materia == 'fisica':
            return redirect('admin_fis_painel')
        if materia == 'matematica':
            return redirect('admin_mat_painel')

        return redirect('home')

    return redirect('home')

# --- SISTEMA DE LOGIN ---
def login_view(request):
    if request.user.is_authenticated:
        # Redirecionamento inteligente baseado no nome do usuário para quem já está logado
        username = request.user.username.lower()
        if 'biologia' in username: return redirect('admin_bio_painel')
        if 'fisica' in username: return redirect('admin_fis_painel')
        if 'matematica' in username: return redirect('admin_mat_painel')
        return redirect('home')

    if request.method == 'POST':
        usuario_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')
        role = request.POST.get('role')  # Captura o valor do <input type="hidden" name="role">
        subject = request.POST.get('subject')  # Captura o valor do <select name="subject">

        # Permite login tanto por nome de usuário quanto por e-mail
        user = authenticate(request, username=usuario_digitado, password=senha_digitada)

        if user is None and usuario_digitado and '@' in usuario_digitado:
            try:
                user_obj = User.objects.get(email__iexact=usuario_digitado)
                user = authenticate(request, username=user_obj.username, password=senha_digitada)
            except User.DoesNotExist:
                user = None

        # Modo de desenvolvimento: se não houver usuário válido, cria/usa um usuário fictício
        if user is None and settings.DEBUG:
            username_ficticio = usuario_digitado or 'demo'
            user, _ = User.objects.get_or_create(
                username=username_ficticio,
                defaults={'email': usuario_digitado or ''}
            )
            # Bypassa autenticação de senha apenas em DEBUG
            user.backend = 'django.contrib.auth.backends.ModelBackend'

        if user is not None:
            login(request, user)
            
            # Se o usuário selecionou "Professor", redireciona conforme a matéria escolhida
            if role == 'teacher':
                if subject == 'biologia':
                    return redirect('admin_bio_painel')
                elif subject == 'fisica':
                    return redirect('admin_fis_painel')
                elif subject == 'matematica':
                    return redirect('admin_mat_painel')
                elif subject == 'quimica':
                    return redirect('admin_quim_painel')
                elif subject == 'historia':
                    return redirect('admin_hist_painel')
                elif subject == 'geografia':
                    return redirect('admin_geo_painel')
                elif subject == 'portugues':
                    return redirect('admin_port_painel')
                else:
                    # Se for professor mas a matéria não tiver painel específico ainda
                    return redirect('home')
            
            # Se for aluno ou qualquer outro caso, vai para a home
            return redirect('home')
        else:
            # Retorna erro para o formulário
            return render(request, 'login.html', {'erro': 'Usuário ou senha incorretos'})
            
    return render(request, 'login.html')

# --- LOGOUT ---
def logout_view(request):
    logout(request)
    return redirect('login')
