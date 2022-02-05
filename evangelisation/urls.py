from django.urls import path
from django.contrib.auth import views as auth_views

from evangelisation import views



app_name="evangelisation"


urlpatterns = [
    path('', views.evangelisation_app_index, name="evangelisation_app_index"),
    path('<int:annee>', views.evangelisation_app_index, name="evangelisation_app_index"),

    path('operations/<str:type_opera>/', 
        views.evangelisation_app_operations, name="evangelisation_app_operations"),

    path('ajouter/<str:type_opera>/', 
        views.evangelisation_app_form_nbre, name="evangelisation_app_form_nbre"),

    path('ajouter/<str:type_opera>/form_nbre=<int:form_nbre>', 
        views.evangelisation_app_multi_form_type_operation, name="evangelisation_app_multi_form_type_operation"),

    path('modifier/<str:type_opera>-elements/', 
            views.evangelisation_app_operations_models_modifier, 
            name="evangelisation_app_operations_models_modifier"), 

    path('modifier/<str:type_opera>/<int:id>/', 
            views.evangelisation_app_operations_modifier, name="evangelisation_app_operations_modifier"),

    path('supprimer/<str:type_opera>-elements/', 
            views.evangelisation_app_operations_models_supprimer, 
            name="evangelisation_app_operations_models_supprimer"), 

    path('supprimer/<str:type_opera>/', 
            views.evangelisation_app_operations_supprimer, name="evangelisation_app_operations_supprimer"),    

    path('recherche/<str:type_opera>/', 
        views.evangelisation_app_operations_recherche, name="evangelisation_app_operations_recherche"),

            
    path('ajouter/<str:type_opera>/form_nbre=<int:form_nbre>', 
        views.evangelisation_app_operations_ajax, name="evangelisation_app_operations_ajax"),


]
