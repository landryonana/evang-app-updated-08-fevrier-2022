from django.urls import path
from django.contrib.auth import views as auth_views

from accounts import views


urlpatterns = [
    path('login/', views.user_login, name="user_login"),
    path('logout/', views.user_logout, name="user_logout"),
    path('comptes/', views.user_comptes, name="user_comptes"),
    path('ajouter-compte/', views.user_register, name="user_register"),
    path('modifier-compte/', views.user_edit, name="user_edit"),
    path('compte/<int:pk>/supprimer', views.user_delete, name="user_delete"),
    path('compte/supprimer', views.user_delete_users, name="user_delete_users"),
    #====================AJAX LEAVE
    path('compte/details', views.user_detail, name="user_detail"),
    path('compte/<int:pk>/details', views.user_detail, name="user_detail"),
    path('recherche-comptes/', views.user_recherche, name="user_recherche"),

    #================================================================================================================================
    #================================================================================================================================
    #===========================RÉINITIALISER LE MOT DE PASSE OU CHANGER=============================================
    path('mot-de-passe-change/', views.change_password, name='password_change'),
    path('mot-de-passe-change/reussi/', views.password_change_done, name='password_change_done'),

    path('reinitialiser-mot-de-passe/',auth_views.PasswordResetView.as_view(
        template_name="registration/password_reset_form.html"
    ),name='password_reset'),
    path('reinitialiser-mot-de-passe/fait/',auth_views.PasswordResetDoneView.as_view(
        template_name="registration/password_reset_done.html"
    ),name='password_reset_done'),
    path('reinitialiser-mot-de-passe/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="registration/password_reset_confirm.html"
        ), name='password_reset_confirm'),
    path('reinitialisation/reuissi/',auth_views.PasswordResetCompleteView.as_view(
        template_name="registration/password_reset_complete.html"
    ), name='password_reset_complete'),

    #=================================================================================================================
    #=================================================================================================================
    #=======================================Login fail=====================================================
    path('tu-dois-etre-sauve/', views.tu_dois_etre_sauver, name="tu_dois_etre_sauver"),
]
