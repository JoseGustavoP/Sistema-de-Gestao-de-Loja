from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('cadastrar_produto/', views.cadastrar_produto, name='cadastrar_produto'),
    path('listar_produtos/', views.listar_produtos, name='listar_produtos'),
    path('produto/delete/<int:id>/', views.delete_produto, name='delete_produto'),
    path('produto/update/<int:id>/', views.update_produto, name='update_produto'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/delete/<int:user_id>/', views.delete_usuario, name='delete_usuario'),
    path('enviar-xml/', views.enviar_xml, name='enviar_xml'),

]