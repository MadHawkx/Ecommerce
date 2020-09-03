from django.urls import path, include
from rest_framework.routers import DefaultRouter
from reviews.api.views import ReviewViewSet

router = DefaultRouter()
router.register("reviews", ReviewViewSet)

urlpatterns = [path("", include(router.urls)),]
