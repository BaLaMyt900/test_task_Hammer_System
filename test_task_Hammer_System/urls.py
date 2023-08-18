from django.contrib import admin
from django.urls import path
from main.views import user_autorization


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_autorization)
]
