from django import forms
from django.conf import settings
import os

from torch import initial_seed

class TrainForm(forms.Form):
    yolo_version = forms.ChoiceField(
        label='模型版本',
        choices=[], # 初始为空，将在__init__中动态设置
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    model_size = forms.ChoiceField(
        label='模型大小',
        choices=[('n', 'Nano'), ('s', 'Small'), ('m', 'Medium'), ('l', 'Large'), ('x', 'Extra Large')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    display_option = forms.ChoiceField(
        label='显卡数量',
        choices=[('0', '无显卡'), ('1', '1张显卡')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    dataset_name = forms.ChoiceField(
        label='数据集',
        choices=[],  # 初始为空，将在__init__中动态设置
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    epochs = forms.IntegerField(
        label='训练轮数',
        initial=1,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    batch= forms.IntegerField(
        label='批次大小',
        initial=8,
        min_value=8,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 构建datasets目录的完整路径，读取支持的数据集
        datasets_dir = os.path.join(settings.BASE_DIR, 'datasets')
        
        # 构建yolo目录的完整路径，读取支持的模型
        yolo_version = os.path.join(settings.BASE_DIR, 'yolo')
        # 检查目录是否存在并获取所有子目录
        if os.path.exists(datasets_dir) and os.path.isdir(datasets_dir):
            subdirectories = [
                d for d in os.listdir(datasets_dir)
                if os.path.isdir(os.path.join(datasets_dir, d))
            ]
            # 设置下拉框选项
            if subdirectories:
                self.fields['dataset_name'].choices = [(d, d) for d in subdirectories]
            else:
                self.fields['dataset_name'].choices = [('none', '无可用数据集目录')]
        else:
            self.fields['dataset_name'].choices = [('none', '数据集目录不存在')]
        
        if os.path.exists(yolo_version) and os.path.isdir(yolo_version):
            subdirectories = [
                d for d in os.listdir(yolo_version)
                if os.path.isdir(os.path.join(yolo_version, d))
            ]
            # 设置下拉框选项
            if subdirectories:
                self.fields['yolo_version'].choices = [(d, d) for d in subdirectories]
            else:
                self.fields['yolo_version'].choices = [('none', '无可用模型')]
        else:
            self.fields['yolo_version'].choices = [('none', '模型目录不存在')]