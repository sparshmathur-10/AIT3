from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('api/todos/', include('api.urls')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 