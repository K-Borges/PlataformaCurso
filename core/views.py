from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# --- PÁGINAS DO ALUNO ---
def home(request):
    return render(request, 'index.html')

def aulas(request):
    return render(request, 'pages/aulas.html')

def materiais(request):
    return render(request, 'pages/materiais.html')

def selecao_simulados(request):
    return render(request, 'pages/selecao-simulados.html')

def simulados_geral(request):
    return render(request, 'pages/simulados-lista.html')


# --- PROFESSOR: BIOLOGIA ---
def admin_bio_painel(request):
    return render(request, 'admin/biologia/painel.html')

def admin_bio_desempenho(request):
    return render(request, 'admin/biologia/desempenho.html')

def admin_bio_ferramentas(request):
    return render(request, 'admin/biologia/ferramentas.html')


# --- PROFESSOR: FÍSICA ---
def admin_fis_painel(request):
    return render(request, 'admin/fisica/painel.html')

def admin_fis_desempenho(request):
    return render(request, 'admin/fisica/desempenho.html')

def admin_fis_ferramentas(request):
    return render(request, 'admin/fisica/ferramentas.html')


# --- PROFESSOR: MATEMÁTICA ---
def admin_mat_painel(request):
    return render(request, 'admin/matematica/painel.html')

def admin_mat_desempenho(request):
    return render(request, 'admin/matematica/desempenho.html')

def admin_mat_ferramentas(request):
    return render(request, 'admin/matematica/ferramentas.html')


# --- SISTEMA DE LOGIN ---
def login_view(request):
    if request.method == 'POST':
        usuario_digitado = request.POST.get('username')
        senha_digitada = request.POST.get('password')
        
        user = authenticate(request, username=usuario_digitado, password=senha_digitada)
        
        if user is not None:
            login(request, user)
            username = user.username.lower()
            
            # Redirecionamento automático baseado no nome do usuário
            if 'biologia' in username:
                return redirect('admin_bio_painel')
            elif 'fisica' in username:
                return redirect('admin_fis_painel')
            elif 'matematica' in username:
                return redirect('admin_mat_painel')
            else:
                return redirect('home')
        else:
            # Retorna erro caso as credenciais estejam incorretas
            return render(request, 'login.html', {'erro': 'Usuário ou senha incorretos'})
            
    return render(request, 'login.html')