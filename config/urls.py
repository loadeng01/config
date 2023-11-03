from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version='v1',
        description="My first blog",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('apps.account.urls')),
    path('api/category/', include('apps.category.urls')),
    path('api/post/', include('apps.post.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/comment/', include('apps.comment.urls'))

]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
