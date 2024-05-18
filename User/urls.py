from django.contrib import admin
from django.urls import path, include
from . import views

privilege_urls = [
    path('privilege/roles/', views.PermissionViews.as_view(), name="get_roles_list"),
    path('privilege/role/delete/<str:id>/', views.RoleDeleteViews.as_view(), name='delete_role'),
    path('privilege/role/delete/', views.RemovePermissionForRole.as_view(), name='delete_role_permission'),
    path('privilege/role/update/', views.PermissionViews.as_view(), name="update_permission_for_role"),
    path('privilege/role/user/update/', views.UpdateRoleForUser.as_view(), name='update_role_for_user'),
    path('privilege/role/', views.PermissionViews.as_view(), name="create_role"),
]

user_url = [
    path('users/<str:id>/delete/', views.AccountInformationView.as_view(), name="Delete"),
    path('users/<str:id>/update/', views.UpdateNameForUser.as_view(), name="Delete"),
    path('users/', views.AccountInformationView.as_view(), name="Users"),
]

urlpatterns = [] + privilege_urls + user_url

