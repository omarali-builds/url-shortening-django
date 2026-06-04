from django.urls import path
from . import views

urlpatterns = [
    path('shorten', views.create_short_url, name='create_short_url'),
    path('shorten/<str:short_code>', views.handle_short_url, name='handle_short_url'),
    path('shorten/<str:short_code>/stats', views.get_url_stats, name='get_url_stats'),
    path('<str:short_code>', views.redirect_to_original, name='redirect_to_original'),
]
