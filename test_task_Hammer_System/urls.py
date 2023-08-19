from django.contrib import admin
from django.urls import path
from main.views import index, Registration, Profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('registration/', Registration.as_view(), name='registration'),
    path('profile/', Profile.as_view())
]
