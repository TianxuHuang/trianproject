from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import HttpResponseRedirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # 初始化中间件时执行一次

    def __call__(self, request):
        # 获取当前请求的路径
        path = request.path_info.lstrip('/')
        print('path=',path)

        # 检查是否是登录页面或不需要登录的路径
        if 'login/' in path or path.startswith('static/'):
            # 不拦截登录页面和静态文件请求
            response = self.get_response(request)
            return response
        
        # 检查用户是否已登录
        if not request.session.get('is_logged_in', False):
            # 用户未登录，重定向到登录页面
            return HttpResponseRedirect(reverse('trainapp:login'))

        
        # 用户已登录，继续处理请求
        response = self.get_response(request)
        return response