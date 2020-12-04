from django.contrib import admin
from django.urls import path, include

app_name = 'main'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
]
