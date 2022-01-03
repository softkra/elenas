from django.urls import path
from .views import (
    CreateUserAPIView,
    CreateTaskAPIView,
    DetailTaskAPIView,
    DeleteTaskAPIView,
    UpdateTaskAPIView,
    ChangeStatusTaskAPIView,
    ListTaskAPIView,
    SearchTaskAPIView
)
from django.urls import include
# SWAGGER
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .swagger import CustomerGeneratorSchema

schema_view = get_schema_view(
    openapi.Info(
        title="Elenas",
        default_version="v1",
        description="Elenas Test - Documentation"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomerGeneratorSchema
)

urlpatterns = [
	path('registration/',CreateUserAPIView.as_view(),name='add-user'),
    path('add-task/', CreateTaskAPIView.as_view(),name='add-task'),
    path('detail-task/<int:pk>/', DetailTaskAPIView.as_view(),name='detail-task'),
    path('delete-task/<int:pk>/', DeleteTaskAPIView.as_view(),name='delete-task'),
    path('update-task/<int:pk>/', UpdateTaskAPIView.as_view(),name='update-task'),
    path('change-task/<int:pk>/', ChangeStatusTaskAPIView.as_view(),name='change-task'),
    path('list-task/', ListTaskAPIView.as_view(),name='list-task'),
    path('search-task/<str:search>/', SearchTaskAPIView.as_view(),name='search-task'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]