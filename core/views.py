from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

# --- PÁGINA DO ALUNO (SPA) ---
@login_required
def home(request):
    """
    Página principal que contém toda a interface do aluno (Aulas, Materiais, Simulados)
    carregada dinamicamente via JavaScript.
    """
    return render(request, 'index.html')


# --- ÁREA DO PROFESSOR: BIOLOGIA ---
@login_required
def admin_bio_painel(request):
    return render(request, 'admin/biologia/painel.html', {"active_page": "dashboard"})


@login_required
def admin_bio_desempenho(request):
    # Usa o mesmo template SPA, iniciando na aba de desempenho
    return render(request, 'admin/biologia/painel.html', {"active_page": "desempenho"})


@login_required
def admin_bio_ferramentas(request):
    # Usa o mesmo template SPA, iniciando na aba de ferramentas/atlas digital
    return render(request, 'admin/biologia/painel.html', {"active_page": "ferramentas"})


# --- ÁREA DO PROFESSOR: FÍSICA ---
@login_required
def admin_fis_painel(request):
    return render(request, 'admin/fisica/painel.html', {"active_page": "dashboard"})


@login_required
def admin_fis_desempenho(request):
    # Usa o mesmo template SPA, iniciando em desempenho
    return render(request, 'admin/fisica/painel.html', {"active_page": "desempenho"})


@login_required
def admin_fis_ferramentas(request):
    # Usa o mesmo template SPA, iniciando em ferramentas
    return render(request, 'admin/fisica/painel.html', {"active_page": "ferramentas"})


# --- ÁREA DO PROFESSOR: MATEMÁTICA ---
@login_required
def admin_mat_painel(request):
    return render(request, 'admin/matematica/painel.html', {"active_page": "dashboard"})


@login_required
def admin_mat_desempenho(request):
    # Usa o mesmo template SPA, iniciando em desempenho
    return render(request, 'admin/matematica/painel.html', {"active_page": "desempenho"})


@login_required
def admin_mat_ferramentas(request):
    # Usa o mesmo template SPA, iniciando em ferramentas
    return render(request, 'admin/matematica/painel.html', {"active_page": "ferramentas"})


# --- ÁREA DO PROFESSOR: OUTRAS MATÉRIAS ---
@login_required
def admin_quim_painel(request):
    return render(request, 'admin/quimica/painel.html')


@login_required
def admin_hist_painel(request):
    return render(request, 'admin/historia/painel.html')


@login_required
def admin_geo_painel(request):
    return render(request, 'admin/geografia/painel.html')


@login_required
def admin_port_painel(request):
    return render(request, 'admin/portugues/painel.html')


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