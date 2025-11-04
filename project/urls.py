from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('doc/', include('doctorandpatientdetails.urls')),
    path('api/', include('employee.urls')),
    path('summernote/',include('django_summernote'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# admin.site.index_title="Hospital Management"
# admin.site.site_header = "Hospital Mangement Admin"
# admin.site.site_title = "Hospital"