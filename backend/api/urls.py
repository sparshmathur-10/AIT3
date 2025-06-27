from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TodoViewSet

router = DefaultRouter()
router.register(r'', TodoViewSet, basename='todo')

urlpatterns = [
    path('', include(router.urls)),
    path('plan/', TodoViewSet.as_view({'post': 'plan'}), name='todo-plan'),
] 