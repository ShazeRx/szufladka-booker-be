from rest_framework.routers import SimpleRouter, Route, DynamicRoute

from szufladka_app.views import KsiazkaView


class KsiazkaRouter(SimpleRouter):
    """Router customowy"""
    # TODO: Remove this custom router maybe and leave default
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'list',
                     'post': 'create',
                     },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'patch': 'update'},
            name='{basename}-update',
            detail=False,
            initkwargs={'suffix': 'Update'}),
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )

    ]


router = KsiazkaRouter()
router.register(r'ksiazki', KsiazkaView)
urlpatterns = router.urls
