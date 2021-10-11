from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import DashboardView, IndexView, ProfileEditView, ProfileView, ShowProfileView, SignUpView, activate, SearchResultsView, test
urlpatterns = [
    path('dashboard',DashboardView.as_view(), name='dashboard'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('',IndexView.as_view(), name='index'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile', ProfileView.as_view(), name= 'profile'),
    path('editprofile', ProfileEditView.as_view(),name= 'editprofile' ),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('<pk>/showprofile', ShowProfileView.as_view(), name= 'showprofile'),
    path('test', test, name='test'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)