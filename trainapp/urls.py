from django.urls import path
from . import views
app_name = 'trainapp'

urlpatterns = [
    path('index/', views.train_index, name='index'),
    path('dotrain/', views.train_form, name='train_form'),
    path('version/', views.version_info, name='version_info'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('export/', views.export_model, name='export_model'),  # 添加导出功能路由
    path('logout/', views.logout, name='logout'),  # 添加注销功能路由

]