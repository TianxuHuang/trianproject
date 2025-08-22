from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('train/', include(('trainapp.urls','trainapp'),namespace='trainapp')),
    path('draw/', include(('draw.urls','draw'),namespace='draw')),  # 添加这一行
]
