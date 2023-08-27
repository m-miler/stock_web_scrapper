from .views import Companies, Prices
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"companies", Companies, basename="companies")
router.register(r"prices", Prices, basename="prices")
urlpatterns = router.urls
