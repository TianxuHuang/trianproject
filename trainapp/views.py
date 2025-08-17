from django.http import HttpResponse
from django.shortcuts import render
from .forms import TrainForm  # 导入表单类
from .train import train_model
from .train import export_model_in_trian
from django.conf import settings
import threading
from datetime import datetime
import sys
import pkg_resources  # 新增导入，用于获取包信息
import os  # 确保已导入os模块
import torch
from django.urls import reverse
from django.http import HttpResponseRedirect

BASE_DIR = settings.BASE_DIR

def train_index(request):
    context={}
    return render(request, 'trainapp/index.html', context)

# 添加表单视图
def train_form(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)
        if form.is_valid():
            # 训练模型
            yolo_version = form.cleaned_data['yolo_version']
            # 训练模型大小
            model_size = form.cleaned_data['model_size']
            # 显卡的数量
            display_option = form.cleaned_data['display_option']
            # 数据集的名称
            dataset_name = form.cleaned_data['dataset_name']
            #训练的轮数
            epochs = form.cleaned_data['epochs']
            #模型绝对路径和文件名
            model_file = BASE_DIR.joinpath('yolo').joinpath(yolo_version).joinpath(yolo_version+model_size+'.pt')
            #批次大小
            batch_size = form.cleaned_data['batch']
            #数据集绝对路径
            dataset_path = BASE_DIR.joinpath('datasets').joinpath(dataset_name).joinpath('data.yaml')

             # 准备传递给模板的参数
            context = {
                'yolo_version': yolo_version,
                'model_size': model_size,
                'dataset_path': dataset_path,
                'epochs': epochs,
                'batch_size': batch_size,
                'train_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }


            #多线程启动训练模型
            thread = threading.Thread(target=train_model_thread, args=(model_file, dataset_path,display_option,batch_size,epochs,dataset_name,yolo_version))
            thread.start()

            return render(request, 'trainapp/train_success.html', context)
            # 处理完成后可以重定向或返回结果
            #return HttpResponse(f"表单提交成功! {model_file}，YOLO版本: {yolo_version}, 模型大小: {model_size}, 显卡选项: {display_option}, 数据集名称: {dataset_name},训练轮数: {epochs},数据集路径: {dataset_path}")
    else:
        form = TrainForm()
    
    return render(request, 'trainapp/form.html', {'form': form})


# 为了方便使用多线程启动训练，特意写了个方法
def train_model_thread(model_file, dataset_path,display_option,batch_size,epochs,dataset_name,yolo_version):
    train_model(model_file, dataset_path,display_option,batch_size,epochs,dataset_name,yolo_version)    

#获取版本信息
def version_info(request):
    # 获取Python版本
    python_version = sys.version.split()[0]
    
    # 项目核心依赖库列表
    required_packages = [
        'django',          # Web框架
        'ultralytics',     # YOLO模型库
        'torch',           # PyTorch深度学习框架
        'numpy',           # 数值计算库
        'pillow',          # 图像处理库
        'openvino',        # OpenVINO格式导出支持
        'onnx'             # ONNX格式导出支持
    ]
    
    # 获取核心库版本信息
    package_versions = []
    for package in required_packages:
        try:
            version = pkg_resources.get_distribution(package).version
            package_versions.append({
                'name': package,
                'version': version,
                'status': 'installed'
            })
        except pkg_resources.DistributionNotFound:
            package_versions.append({
                'name': package,
                'version': '未安装',
                'status': 'missing'
            })
    
    context = {
        'python_version': python_version,
        'packages': package_versions,
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return render(request, 'trainapp/version.html', context)
def about(request):
    return render(request, 'trainapp/about.html')

#导出模型
def export_model(request):
    # 获取runs目录下的所有子目录
    runs_path = os.path.join(settings.BASE_DIR, 'runs')
    run_directories = []
    
    if os.path.exists(runs_path) and os.path.isdir(runs_path):
        run_directories = [
            d for d in os.listdir(runs_path)
            if os.path.isdir(os.path.join(runs_path, d))
        ]
    
    if request.method == 'POST':
        # 这里将在后续实现导出逻辑
        selected_run = request.POST.get('run_directory')
        export_format = request.POST.get('export_format')
        #导出模型的路径
        export_path = BASE_DIR.joinpath('runs').joinpath(selected_run).joinpath('train').joinpath('weights').joinpath('best.pt')
        print(f'export_path:{export_path}')



        if export_format=='engine':
        # 检查是否有可用显卡
            if not torch.cuda.is_available():     
                context={
                    'error_message':'导出为engine格式需要GPU支持，请确保有可用显卡。'
                }   
                        
                return render(request, 'trainapp/error.html', context)                
        # 保留原有的engine格式，不转换为onnx
        # export_format='onnx'
        #导出模型
        export_model_in_trian(export_path,export_format)
        # 导出完成后，刷新页面      
        
        return render(request, 'trainapp/success.html')


    
    context = {
        'run_directories': run_directories,
        'export_formats': [('onnx', 'ONNX'), ('openvino', 'OpenVINO'), ('engine', 'TensorRT Engine')]
    }
    return render(request, 'trainapp/export.html', context)

def login(request):
    if request.method == 'POST':        
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username=='13978769766' and password=='gxcvu9527':
            request.session['is_logged_in'] = True
            request.session['username'] = username           
            return render(request, 'trainapp/index.html')
        else:
            context={
                'error':'用户名或密码错误'
            }
            return render(request, 'trainapp/login.html', context)
    context={}
    return render(request, 'trainapp/login.html', context)

def logout(request):
    # 清除用户登录状态
    request.session.flush()
    return HttpResponseRedirect(reverse('trainapp:login'))

