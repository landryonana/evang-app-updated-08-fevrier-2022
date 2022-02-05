from django.urls import path

from rapport import views




app_name="rapport"

urlpatterns = [
    path('', views.rapport_app_index, name='rapport_app_index'),
    path('generate-pdf/<str:orientation>', views.generate_pdf, name='generate_pdf'),
    path('generate-pdf/<str:orientation>/<int:annee>/', views.generate_pdf, name='generate_pdf'),
    path('<int:pk>/detail', views.rapport_app_detail, name='rapport_app_detail'),
]