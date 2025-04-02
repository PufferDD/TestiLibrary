from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('works/', views.work_list, name='work_list'),
    path('works/<int:pk>/', views.work_detail, name='work_detail'),
    path('works/<int:pk>/borrow/', views.borrow_work, name='borrow_work'),
    path('loans/', views.my_loans, name='my_loans'),
    path('loans/<int:loan_id>/return/', views.return_work, name='return_work'),
    path('admin/loans/', views.all_loans, name='all_loans'),
]