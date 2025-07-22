from django.contrib import admin
from django.urls import path, include  # 添加include导入

urlpatterns = [
    path('admin/', admin.site.urls),
    path('train/', include('trainapp.urls')),  # 添加这行配置
]
