from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('QFSci_manager.api.urls_info')),
    path('', include('QFSci_manager.api.urls_user')),
]
