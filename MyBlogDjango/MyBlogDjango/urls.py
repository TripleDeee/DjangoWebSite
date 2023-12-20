from django.contrib import admin
from django.urls import path, include  # Добавлен include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]