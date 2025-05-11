from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'departments', views.DepartmentInfoViewSet)
router.register(r'sections', views.SectionInfoViewSet)
router.register(r'requests', views.InventoryRequestViewSet, basename='inventoryrequest')

urlpatterns = [
    path('api/', include(router.urls)),
    path('return-product/', views.ReturnProductView.as_view(), name='return-product'),
]
