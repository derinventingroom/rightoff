from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list/', views.expense_list, name='expense_list'),

    path(
        'export/',
        views.export_csv,
        name='export_csv'
    ),
    path(
        'delete/<int:expense_id>/',
        views.delete_expense,
        name='delete_expense'
    ),
    path(
        'edit/<int:expense_id>/',
        views.edit_expense,
        name='edit_expense'
    ),
]