
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from restframework import views
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views


router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('dashboard.urls')),
    path('',include('product.urls')),
    path('',include('purchase.urls')),
    path('',include('notifications.urls')),
    path('', include('social_django.urls', namespace='social')),

    path('api/auth/', include('knox.urls')),
    path('api/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token, name='api-tokn-auth'),
    path('api-auth/', include('rest_framework.urls')),
    path('apitest/',include('restframework.urls')),
    path('docs/', include_docs_urls(title='Todo Api')),
    
    
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]