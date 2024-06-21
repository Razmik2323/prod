from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
)


app_name = 'myauth'

urlpatterns = [
    path('login/',
         LoginView.as_view(template_name='myauth/login.html',
                           redirect_authenticated_user=True
                           ),
         name='login'),
    path('cookie/get/', get_cookie_view, name='cookie-get'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),
    path('session/get/', get_session_view, name='get-session'),
    path('session/set/', set_session_view, name='set-session'),
    path('logout/', MyLogoutView.as_view(), name='logout'),

]
