# Settings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # List views
    path('functions/', views.functions_list, name='functions_list'),
    path('types_of_service/', views.types_of_service_list, name='types_of_service_list'),
    path('services/', views.services_list, name='services_list'),
    path('responsibilities/', views.responsibilities_list, name='responsibilities_list'),
    path('permission-groups/', views.permission_groups_list, name='permission_groups_list'),
    path('roles/', views.roles_list, name='roles_list'),

    # Create views
    path('functions/add/', views.create_function, name='create_function'),
    path('types_of_service/add/', views.create_type_of_service, name='create_type_of_service'),
    path('services/add/', views.create_service, name='create_service'),
    path('responsibilities/add/', views.create_responsibility, name='create_responsibility'),
    path('permission-groups/add/', views.create_permission_group, name='create_permission_group'),
    path('roles/add/', views.create_role, name='create_role'),

    # Edit views
    path('functions/edit/<uuid:pk>/', views.edit_function, name='edit_function'),
    path('types_of_service/edit/<uuid:pk>/', views.edit_type_of_service, name='edit_type_of_service'),
    path('services/edit/<uuid:pk>/', views.edit_service, name='edit_service'),
    path('responsibilities/edit/<uuid:pk>/', views.edit_responsibility, name='edit_responsibility'),
    path('permission-groups/edit/<uuid:pk>/', views.edit_permission_group, name='edit_permission_group'),
    path('roles/edit/<uuid:pk>/', views.edit_role, name='edit_role'),

    # Delete views
    path('functions/delete/<uuid:pk>/', views.delete_function, name='delete_function'),
    path('types_of_service/delete/<uuid:pk>/', views.delete_type_of_service, name='delete_type_of_service'),
    path('services/delete/<uuid:pk>/', views.delete_service, name='delete_service'),
    path('responsibilities/delete/<uuid:pk>/', views.delete_responsibility, name='delete_responsibility'),
    path('permission-groups/delete/<uuid:pk>/', views.delete_permission_group, name='delete_permission_group'),
    path('roles/delete/<uuid:pk>/', views.delete_role, name='delete_role'),
    # Detail views
    path('functions/<uuid:pk>/', views.function_detail, name='function_detail'),
    path('types_of_service/<uuid:pk>/', views.type_of_service_detail, name='type_of_service_detail'),
    path('services/<uuid:pk>/', views.service_detail, name='service_detail'),
    path('responsibilities/<uuid:pk>/', views.responsibility_detail, name='responsibility_detail'),
    path('permission-groups/<uuid:pk>/', views.permission_group_detail, name='permission_group_detail'),
    path('roles/<uuid:pk>/', views.role_detail, name='role_detail'),
]
