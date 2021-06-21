from django.urls import include, path

from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path("portfolio/", include("portfolio.urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),

    #    url(r'^accounts/login', 'django.contrib.auth.views.login')),
    # Examples:
    # url(r'^$', 'testproject.views.home', name='home'),
    # url(r'^testproject/', include('testproject.foo.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
