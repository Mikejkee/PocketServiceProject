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
router.register('api/client', api.ClientViewSet, basename="Client")
router.register('api/product', api.ProductViewSet, basename="Product")
router.register('api/order', api.OrderViewSet, basename="Order")
router.register('api/company', api.CompanyViewSet, basename="Order")
router.register('api/agent', api.AgentViewSet, basename="Agent")
router.register('api/price', api.PriceViewSet, basename="Price")

urlpatterns = router.urls
urlpatterns += [
    re_path(r'^swagger(?P<id>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # Person
    path('api/person/info', api.APIPersonInfoByTelegramID.as_view(), name='person_info'),

    # Client
    path('api/client/info', api.APIClientInfoByTelegramID.as_view(), name='client_info'),

    # Agent
    path('api/agent/info', api.APIAgentInfoByTelegramID.as_view(), name='agent_info'),

    # Company
    path('api/company_by_user/info', api.APICompanyInfoByTelegramID.as_view(), name='company_info'),

    # Prices
    path('api/prices_by_agent/info', api.APIPPricesInfoByAgentID.as_view(), name='prices_info'),

    #Order
    path('api/orders_by_agent/info', api.APIPOrdersInfoByAgentTelegramID.as_view(), name='orders_by_agent_info'),
    path('api/orders_by_client/info', api.APIPOrdersInfoByClientTelegramID.as_view(), name='orders_by_client_info'),
    path('api/orders_by_client/create', api.APIPOrdersCreateByClient.as_view(), name='orders_create_by_client'),

    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('main/', IndexView.as_view(), name='main'),
    path('showcase/', ShowcaseView.as_view(), name='showcase'),
    path('profile/', ProfileView.as_view(), name='profile'),
    # path("controllers/<task_id>/", get_status, name="get_status"),
    # path("controllers/", run_task, name="run_task"),
]
