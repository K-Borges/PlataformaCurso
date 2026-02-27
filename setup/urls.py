from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    # --- ADMIN DJANGO ---
    path('admin_django/', admin.site.urls),

    # --- AUTENTICAÇÃO ---
    # Usando a view personalizada de login e a view de logout definida no views.py
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # --- PORTAL DO ALUNO (SPA) ---
    path('', views.home, name='home'),

    # --- PROFESSOR: BIOLOGIA ---
    path('professor/biologia/painel/', views.admin_bio_painel, name='admin_bio_painel'),
    path('professor/biologia/desempenho/', views.admin_bio_desempenho, name='admin_bio_desempenho'),
    path('professor/biologia/ferramentas/', views.admin_bio_ferramentas, name='admin_bio_ferramentas'),

    # --- PROFESSOR: FÍSICA ---
    path('professor/fisica/painel/', views.admin_fis_painel, name='admin_fis_painel'),
    path('professor/fisica/desempenho/', views.admin_fis_desempenho, name='admin_fis_desempenho'),
    path('professor/fisica/ferramentas/', views.admin_fis_ferramentas, name='admin_fis_ferramentas'),

    # --- PROFESSOR: MATEMÁTICA ---
    path('professor/matematica/painel/', views.admin_mat_painel, name='admin_mat_painel'),
    path('professor/matematica/desempenho/', views.admin_mat_desempenho, name='admin_mat_desempenho'),
    path('professor/matematica/ferramentas/', views.admin_mat_ferramentas, name='admin_mat_ferramentas'),

    # --- PROFESSOR: OUTRAS MATÉRIAS ---
    path('professor/quimica/painel/', views.admin_quim_painel, name='admin_quim_painel'),
    path('professor/historia/painel/', views.admin_hist_painel, name='admin_hist_painel'),
    path('professor/geografia/painel/', views.admin_geo_painel, name='admin_geo_painel'),
    path('professor/portugues/painel/', views.admin_port_painel, name='admin_port_painel'),
]