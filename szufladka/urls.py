from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('autoryzacja/', include('autoryzacja.urls')),
    path('szufladka/', include('szufladka_app.urls'))
]
