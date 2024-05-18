from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('users/<str:id>/delete/', views.DeleteUserByUsernameView.as_view(), name="Delete"),
    path('users/', views.UsersViews.as_view(), name="Users"),
    path('users/find/', views.find_by_username, name='find_by_username'),
    path('users/<int:id>/update/', views.update_user, name='update_user'),
    path('users/role/create/', views.createRole.as_view(), name="CreateRole"),
    
    path('privilege/role/user/update', views.set_user_role, name='set_user_role'), 
    path('privilege/roles/', views.get_roles, name="get_roles"),
    path('privilege/role/update', views.update_role_permission, name="update_role_permission"),
    path('privilege/role/delete/', views.remove_role_permission, name='remove_role_permission'),
    path('privilege/role/delete/<int:role_id>/', views.delete_role, name='delete_role'),
]
