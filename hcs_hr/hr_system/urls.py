from django.urls import path, re_path
from . import views, api
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Hr_system API",
      default_version='v1',
      contact=openapi.Contact(email="contact@snippets.local"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()
router.register('admins', api.AdminsViewSet, basename="Administrator")
router.register('clients', api.ClientViewSet, basename="Client")
router.register('products', api.ProductViewSet, basename="Product")
router.register('orders', api.OrderViewSet, basename="Order")
urlpatterns = router.urls
urlpatterns += [
    re_path(r'^swagger(?P<id>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
