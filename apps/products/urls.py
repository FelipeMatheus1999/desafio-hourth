from rest_framework.routers import DefaultRouter

from apps.products.views import ProductsViewSet


router = DefaultRouter()
router.register("products", ProductsViewSet)
urlpatterns = router.urls
