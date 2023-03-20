from django.conf.urls import include
from django.urls import re_path
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'try.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    re_path(r'^admin/', admin.site.urls),
    re_path(r'^stock/', include(('stock.urls', 'stock'), namespace="stock")),
]