from django.contrib import admin
from django.urls import path, include
from api.views import StartPage, EnterReferralCode


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rest_framework.urls')),
    path('', StartPage.as_view()),
    path('add_referral/', EnterReferralCode.as_view())
]
