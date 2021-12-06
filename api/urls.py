from django.urls import path,include
from . import views
urlpatterns = [
    path('api/authentication',views.Authentication.as_view()),
    path('api/accounts',views.Accounts.as_view()),
    path('api/store',views.store.as_view())
]
