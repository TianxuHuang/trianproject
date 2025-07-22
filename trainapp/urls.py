from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.train_index, name='index'),
    path('dotrain/', views.train_form, name='train_form'),
    path('version/', views.version_info, name='version_info'),
    path('about/', views.about, name='about'),
    path('export/', views.export_model, name='export_model'),  # 添加导出功能路由
]