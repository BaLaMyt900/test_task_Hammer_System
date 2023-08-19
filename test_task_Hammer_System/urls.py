from django.contrib import admin
from django.urls import path, include
from api.views import StartPage, EnterReferralCode


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('api/', StartPage.as_view()),
    path('api/add_referral/', EnterReferralCode.as_view())
]
