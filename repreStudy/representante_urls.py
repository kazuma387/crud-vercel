from django.urls import path
from . import views

urlpatterns = [
    path('', views.representante_index, name='representante'),
    path('<letter>', views.representante_index, name='representante'),
    path('view/<int:id>', views.representante_view, name='representante_view'),
    path('edit/<int:id>', views.representante_edit, name='representante_edit'),
    path('create/', views.representante_create, name='representante_create'),
    path('delete/<int:id>', views.representante_delete, name='representante_delete'),
    path('confirm_delete/<int:id>/', views.representante_confirm_delete, name='representante_confirm_delete'),
]