"""
URL configuration for smarthome project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from myapp import views
from smarthome import settings

urlpatterns = [
    path('home/',views.home),
    path('login_view/',views.login_view),
    path('login_post/',views.login_post),
    path('architect_home/',views.architect_home),

    path('logout_view/',views.logout_view),

    path('change_pass/',views.change_pass),
    path('change_post/',views.change_post),

    path('register/',views.register),
    path('register_post/',views.register_post),

    path('view_architect/',views.view_architect),
    path('view_mobile_users/',views.view_mobile_users),
    path('approve_architect/<id>',views.approve_architect),
    path('reject_architect/<id>',views.reject_architect),
    path('ad_approved/',views.ad_approved),
    path('ad_rejected/',views.ad_rejected),

    path('view_complaints/',views.view_complaints),
    path('admin_reply/<id>',views.admin_reply),
    path('admin_reply_post/',views.admin_reply_post),

    path('view_arch_prof/',views.view_arch_prof),
    path('edit_architect/<id>',views.edit_architect),
    path('ed_architect_post/<id>',views.ed_architect_post),

    path('add_work/',views.add_work),
    path('add_work_post/',views.add_work_post),
    path('view_add_work/',views.view_add_work),
    path('delete_work/<id>',views.delete_work),
    path('edit_works/<id>',views.edit_works),
    path('ed_works_post/<id>',views.ed_works_post),

    path('view_request/',views.view_request),
    path('accept_request/<id>',views.accept_request),
    path('reject_request/<id>',views.reject_request),
    path('ad_accept/',views.ad_accept),

    path('view_chat/<id>',views.view_chat),
    path('send_message/',views.send_message),
    path('fetch_chat/',views.fetch_chat),


    path('register_user/',views.register_user),
    path('user_login/',views.user_login),
    path('view_user_profile/',views.view_user_profile),
    path('get_user_edit/',views.get_user_edit),
    path('update_user_profile/',views.update_user_profile),
    path('user_view_architect/',views.user_view_architect),


    path('view_architect_design/',views.view_architect_design),
    path('user_send_req/',views.user_send_req),

    path('send_complaints/',views.send_complaints),
    path('reply_byst/',views.reply_byst),


    path('user_chat/',views.user_chat),
    path('send_user/',views.send_user),

    # path('generate_interior/', views.interior_api, name='generate_interior'),
    #
    #
    # path('aichatbot/',views.aichatbot),




]