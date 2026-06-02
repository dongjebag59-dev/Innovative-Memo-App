from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/memo/', permanent=False)),
    path('admin/', admin.site.urls),
    path('memo/', include('memo.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
]
