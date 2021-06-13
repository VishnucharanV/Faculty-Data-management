from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('',views.first,name="first"),
    path('home',views.home,name="home"),
    path('audio',views.Audio1,name="audio"),
    path('personal',views.personal,name="personal"),
    path('eveat',views.eveat,name="eveat"),
    path('evcon',views.evcon,name="evcon"),
    path('awards',views.awards,name="awards"),
    path('report',views.report,name="report"),
    path('finalaudio',views.audio_list,name="finalaudio"),
    path('textpage',views.textpage,name="textpage"),
    path('login',views.login,name="login"),
    path('logout',views.logout,name="logout"),
    path('email',views.email,name="email"),
    path('whatsapp',views.whatsapp,name="whatsapp"),
    path('awards/update',views.update,name="update"),
    path('eveat/update1',views.update1,name="update1"),
    path('evcon/update2',views.update2,name="update2"),
    path('awards/update/updateawards',views.updateawards,name="updateawards"),
    path('eveat/update1/updateeveat',views.updateeveat,name="updateeveat"),
    path('evcon/update2/updateevcon',views.updateevcon,name="updateevcon"),
    path('report/submit',views.submit,name="submit"),
    url(r'^pdf/$',views.generate_pdf,name="gen")
]

