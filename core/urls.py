from typing import Union

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import URLResolver, include, path
from rest_framework.routers import SimpleRouter

from store.views import BookViewSet, UserBookRelationView, auth

URL = Union[URLResolver, object]
URLList = list[URL]

router = SimpleRouter()

router.register(r'book', BookViewSet)
router.register(r'book_relation', UserBookRelationView)

urlpatterns: URLList = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path(settings.ADMIN_BASE_URL, admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
]

urlpatterns += router.urls

if settings.DEBUG:
    import mimetypes

    import debug_toolbar

    mimetypes.add_type('application/javascript', '.js', True)

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns  # type: ignore
