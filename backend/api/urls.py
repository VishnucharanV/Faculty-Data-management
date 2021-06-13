from django.urls import path
from backend.api.views import awards_api,awards_details
from .import views

app_name = 'blog'
urlpatterns = [
        path('awards_api/',views.awards_api,name="awards_api"),
        path('detailapi/<int:pk>',views.awards_details,name="detailapi"),
        path('awards_apidec/',views.awards_apidec,name="awards_apidec"),
        path('detailapidec/<int:pk>',views.awards_detailsdec,name="detailapidec"),
]
