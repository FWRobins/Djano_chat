from django.urls import path

from chat import views

# create app name to dynamicaly cal urls like 'dashboard_app:register'
app_name = 'chat_app'

urlpatterns = [
    path('', views.index, name='index'),

    path('register/', views.register, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),

    # resset password
    path("password_reset/", views.password_reset_request, name="password_reset"),

    path('<str:room_name>/', views.room, name='room'),
]
