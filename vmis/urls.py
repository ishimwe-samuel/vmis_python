from rest_framework import routers
from .api import VaccineListViewSet, VaccineStockViewSet
router = routers.DefaultRouter()
router.register('api/vaccines', VaccineListViewSet)
router.register('api/stock', VaccineStockViewSet)
urlpatterns = router.urls
