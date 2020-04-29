# Django imports
from django.contrib import admin
from django.urls import path, include

# Project imports
from neuroflow.accounts import urls as accounts_urls
from neuroflow.moods import urls as moods_urls
from neuroflow.moods.api import urls as api_urls


# URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(accounts_urls)),
    path('', include(moods_urls)),
    path('mood/', include(api_urls)),
]
