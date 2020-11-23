"""currency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from account import views

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('rate/', include('rate.urls')),
    path('account/', include('account.urls')),
    path('my_password_change/<int:pk>', views.MyPasswordChangeView.as_view(), name='my_password_change'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))

handler404 = 'rate.views.my_custom_page_not_found_view'
handler500 = 'rate.views.my_custom_error_view'

# from django.utils.functional import curry
# from django.views.defaults import server_error, page_not_found
# handler404 = curry(page_not_found, template_name='errs/404.html')
# handler500 = curry(server_error, template_name='errs/505.html')
