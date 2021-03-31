from django.urls import path
from . import views
app_name='fbapp'
urlpatterns = [
    path('', views.fn_index,name="index"),
    path('login/',views.fn_login,name="login"),
    path('home/',views.fn_home,name="home"),
    path('changepassword/',views.fn_changepassword,name="changepassword"),
    path('viewprofile/',views.fn_viewprofile,name='viewprofile'),
    path('addfriend/',views.fn_addfriend,name="addfriend"),
    path('viewfriend/',views.fn_viewfriend,name='viewfriend'),
    path('sendrequest/',views.fn_sendrequest,name='sendrequest'),
    path('acceptrequest/',views.fn_acceptrequest,name='acceptrequest'),
    path('cancelrequest/',views.fn_cancelrequest,name='cancelrequest'),
    path('getdata/',views.fn_data),
    path('getdatahtml',views.fn_getdata),
    path('sendMsg/', views.post_data),
]