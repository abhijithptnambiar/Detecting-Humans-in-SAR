"""Detect_Hu_In_SAR URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django.contrib
from django.urls import path

from Detect_Hu_In_SAR_app import views

urlpatterns = {

    path('', views.log),
    path('log_post',views.log_post),
    path('logout',views.logout),
    path('addrt',views.addrt),
    path('edit/<id>',views.edit),
    path('edit_post/<id>',views.edit_post),
    path('changep',views.changep),
    path('changep_post',views.changep_post),
    path('viewf',views.viewf),
    path('viewrt',views.viewrt),
    path('viewst/<id>',views.viewst),
    path('workall/<id>',views.workall),
    path('workall_post/<id>',views.workall_post),
    path('adminhome',views.adminhome),
    path('addrt_post',views.addrt_post),
    path('deletert/<id>',views.deletert),

    path('login_res',views.login_res),
    path('view_work_allocation',views.view_work_allocation),
    path('view_detection',views.view_detection),
    path('send_feedback',views.send_feedback),
    path('change_password',views.change_password),
    path('update_status',views.update_status),
    path('payment_method/<id>/<am>',views.payment_method),
    path('payment_submit/<id>/<am>',views.payment_submit),
    path('default/<id>',views.default),
    path('online/<id>/<amount>',views.online),
    path('forgot_password',views.forgot_password),
    path('forgot_passwordbuttonclick',views.forgot_passwordbuttonclick),
    path('otp',views.otp),
    path('otpbuttonclick',views.otpbuttonclick),
    path('detect_human',views.detect_human),
    path('upload_gallery',views.upload_gallery),
    path('upload_gallery_post',views.upload_gallery_post),
    path('generate_password',views.generate_password),
    path('real_detection',views.real_detection),

}
