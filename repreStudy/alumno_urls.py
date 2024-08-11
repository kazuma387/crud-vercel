from django.urls import path
from . import views

urlpatterns = [
    path('', views.alumno_index, name='alumno'),
    path('<letter>', views.alumno_index, name='alumno'),
    path('view/<int:id>', views.alumno_view, name='alumno_view'),
    path('edit/<int:id>', views.alumno_edit, name='alumno_edit'),
    path('create/', views.alumno_create, name='alumno_create'),
    path('delete/<int:id>', views.alumno_delete, name='alumno_delete'),
    path('confirm_delete/<int:id>/', views.alumno_confirm_delete, name='alumno_confirm_delete'),    
]