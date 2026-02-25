from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
    return render(request, 'admin/biologia/painel.html')

@login_required
def admin_bio_desempenho(request):
    return render(request, 'admin/biologia/desempenho.html')

@login_required
def admin_bio_ferramentas(request):
    return render(request, 'admin/biologia/ferramentas.html')


# --- ÁREA DO PROFESSOR: FÍSICA ---
@login_required
def admin_fis_painel(request):
    return render(request, 'admin/fisica/painel.html')

@login_required
def admin_fis_desempenho(request):
    return render(request, 'admin/fisica/desempenho.html')

@login_required
def admin_fis_ferramentas(request):
    return render(request, 'admin/fisica/ferramentas.html')


# --- ÁREA DO PROFESSOR: MATEMÁTICA ---
@login_required
def admin_mat_painel(request):
    return render(request, 'admin/matematica/painel.html')

@login_required
def admin_mat_desempenho(request):
    return render(request, 'admin/matematica/desempenho.html')

@login_required
def admin_mat_ferramentas(request):
    return render(request, 'admin/matematica/ferramentas.html')


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
        subject = request.POST.get('subject') # Captura o valor do <select name="subject">
        
        user = authenticate(request, username=usuario_digitado, password=senha_digitada)
        
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
                # Adicione outros elif para Química, História, etc., se houver views para eles
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
