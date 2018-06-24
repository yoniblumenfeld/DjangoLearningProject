from django.conf.urls import url,include
from firstapp.views import home

urlpatterns = [
    url(r'^home/$',home,name="home")
]