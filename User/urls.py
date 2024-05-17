from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('users/<str:id>/delete/', views.DeleteUserByUsernameView.as_view(), name="Delete"),
    path('users/role/create/', views.createRole.as_view(), name="CreateRole"),
    path('users/', views.UsersViews.as_view(), name="Users"),
    path('privilege/roles/', views.getRole.as_view(), name="Roles"),
    path('privilege/roles/update_permission', views.update_role_permission, name="update_role_permission")
]
