@echo off
echo Starting Django development server...

REM �������⻷�� (�������)
REM ��������Ŀʹ�������⻷�����뽫��һ�е� "venv\Scripts\activate" �滻Ϊ�����⻷����ʵ��·��
REM ���磺call C:\Users\YourUser\project_name\venv\Scripts\activate
REM ���û��ʹ�����⻷������ɾ����ע�͵���һ��
REM call envs\Scripts\activate

REM ���� Django ����������
start python manage.py runserver

timeout /t 8 >nul
REM �ȴ�����������������ȴ� 5 �룬����Ը�����Ҫ����

echo Opening browser...
start http://127.0.0.1:8000

echo Script finished.