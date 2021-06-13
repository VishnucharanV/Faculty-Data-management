"""faculty URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from backend import views as backend_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from backend.api import views as api_views
#REST FRAMEWORK urls

urlpatterns = [
    path('awards_api/',api_views.awards_api,name="awards_api"),
    path('awards_apidec/',api_views.awards_apidec,name="awards_apidec"),
    path('detailapi/<int:pk>/',api_views.awards_details,name="detailapi"),
        path('detailapidec/<int:pk>',api_views.awards_detailsdec,name="detailapidec"),
    path('admin/', admin.site.urls),
    path('',include('backend.urls')),
    path('home/',backend_views.home,name="home"),
    path('personal/',backend_views.personal,name="personal"),
    path('eveat/',backend_views.eveat,name="eveat"),
    path('evcon/',backend_views.evcon,name="evcon"),
    path('awards/',backend_views.awards,name="awards"),
    path('audio/',backend_views.Audio1,name="audio"),
    path('login/',backend_views.login,name="login"),
    path("finalaudio/",backend_views.audio_list,name="finalaudio"),
    path("textpage/",backend_views.textpage,name="textpage"),
    path('report/',backend_views.report,name="report"),
    path('email/',backend_views.email,name="email"),
    path('whatsapp/',backend_views.whatsapp,name="whatsapp"),
    path('report/submit',backend_views.submit,name="submit"),
    path('logout/',backend_views.logout,name="logout"),
    path('awards/update/',backend_views.update,name="update"),
    path('eveat/update1/',backend_views.update1,name="update1"),
    path('evcon/update2/',backend_views.update2,name="update2"),
    path('awards/update/updateawards',backend_views.updateawards,name="updateawards"),
    path('eveat/update1/updateeveat',backend_views.updateeveat,name="updateeveat"),
    path('evcon/update2/updateevcon',backend_views.updateevcon,name="updateevcon"),
    url(r'^pdf/$',backend_views.generate_pdf,name="gen")
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
