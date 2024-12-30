from home import views
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("",views.index,name='home'),
    path('generate-script/', views.generate_script, name='generate_script'),
    path('save_script/', views.save_script, name='save_script'),
    path('saved_scripts/', views.saved_scripts, name='saved_scripts'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)