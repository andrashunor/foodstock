"""foodstock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(title='Foodstock API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer], public=True)

urlpatterns = [
    path('api-docs/', schema_view, name='api-docs'),
    path('api/', include('api.food.urls')),
    path('api/', include('api.image.urls')),
    path('api/', include('api.auth.urls')),
    path('api/', include('api.ingredient.urls')),
    path('', include('frontend.urls')),
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) 
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


