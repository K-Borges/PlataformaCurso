"""
URL configuration for setup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    # --- ADMIN ---
    path('admin_django/', admin.site.urls),

    # --- PÁGINAS DO ALUNO (Pasta: pages/) ---
    path('', views.home, name='home'),
    path('aulas/', views.aulas, name='aulas'),
    path('materiais/', views.materiais, name='materiais'),
    path('simulados-selecao/', views.selecao_simulados, name='selecao_simulados'),
    path('simulados-lista/', views.simulados_geral, name='simulados_lista'),

    # --- LOGIN ---
    path('login/', views.login_view, name='login'),

    # --- PROFESSOR: BIOLOGIA (Pasta: admin/biologia/) ---
    path('professor/biologia/painel/', views.admin_bio_painel, name='admin_bio_painel'),
    path('professor/biologia/desempenho/', views.admin_bio_desempenho, name='admin_bio_desempenho'),
    path('professor/biologia/ferramentas/', views.admin_bio_ferramentas, name='admin_bio_ferramentas'),

    # --- PROFESSOR: FÍSICA (Pasta: admin/fisica/) ---
    path('professor/fisica/painel/', views.admin_fis_painel, name='admin_fis_painel'),
    path('professor/fisica/desempenho/', views.admin_fis_desempenho, name='admin_fis_desempenho'),
    path('professor/fisica/ferramentas/', views.admin_fis_ferramentas, name='admin_fis_ferramentas'),

    # --- PROFESSOR: MATEMÁTICA (Pasta: admin/matematica/) ---
    path('professor/matematica/painel/', views.admin_mat_painel, name='admin_mat_painel'),
    path('professor/matematica/desempenho/', views.admin_mat_desempenho, name='admin_mat_desempenho'),
    path('professor/matematica/ferramentas/', views.admin_mat_ferramentas, name='admin_mat_ferramentas'),
]