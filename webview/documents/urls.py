from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views
urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='index'),
    url(r'^upload$', views.UploadFormView.as_view(), name='upload'),
]
