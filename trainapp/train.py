from ultralytics import YOLO

def train_model(model_file, dataset_path,display_option,batch_size,epochs,dataset_name,yolo_version):



    '''
    # model.train()方法是YOLO模型训练的核心接口
    # 参数说明：
    # data: 指定数据集配置文件路径或名称
    # batch: 批次大小，每次迭代处理的图像数量
    # epochs: 训练轮数，整个数据集将被训练的次数
    # name: 训练任务名称，用于结果文件夹命名
    # device: 训练设备，'0'表示使用第1个GPU，'cpu'表示使用CPU
    # project: 训练结果保存的根目录
    # workers: 数据加载的工作进程数
    # optimizer: 优化器选择，'auto'表示自动选择合适的优化器
    # imgsz: 输入图像大小，所有图像将被调整为该尺寸   
    '''
    device = '0' if display_option == '1' else 'cpu'
    print('加载模型开始...')
    model = YOLO(model_file)
    print('加载模型完成...')
    print('训练模型开始...')
    results = model.train(
        data=dataset_path,
        batch=batch_size,
        epochs=epochs,
        #name=dataset_name,
        device=device,
        project='runs/'+dataset_name+'_'+yolo_version,
        workers=8,
        optimizer="auto",
        imgsz=640
    )
    print('训练模型完成...')
    #print('模型评估开始...')
    #results = model.val()
    #print('模型评估完成...')
    return results

import torch

def export_model_in_trian(model_file,export_format):
            
    print('导出模型开始...')
    model = YOLO(model_file)
    model.export(format=export_format)
    print('导出模型完成...')