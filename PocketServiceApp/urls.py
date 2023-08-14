from django.urls import path, re_path
from . import api
from PocketServiceApp.controllers.html_views import ShowcaseView, IndexView, ProfileView
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="PocketServiceProject API",
      default_version='v1',
      contact=openapi.Contact(email="contact@snippets.local"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()
# router.register('/api/admins', api.AdminsViewSet, basename="Administrator")
router.register('api/person', api.PersonViewSet, basename="Person")
router.register('api/clients', api.ClientViewSet, basename="Client")
router.register('api/products', api.ProductViewSet, basename="Product")
router.register('api/orders', api.OrderViewSet, basename="Order")

urlpatterns = router.urls

urlpatterns += [
    re_path(r'^swagger(?P<id>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Person
    path('api/person/info', api.APIPersonInfoByTelegramID.as_view(), name='person_info'),
    # path('api/person/edit_info', api.APIPersonEditByTelegramID.as_view(), name='person_info'),

    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('main/', IndexView.as_view(), name='main'),
    path('showcase/', ShowcaseView.as_view(), name='showcase'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # path("controllers/<task_id>/", get_status, name="get_status"),
    # path("controllers/", run_task, name="run_task"),
]
