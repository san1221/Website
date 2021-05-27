from django.urls import path
from core import views

urlpatterns = [
    path('',views.home,name = 'home'),
    path('aboutus',views.aboutus, name='aboutus'),
    path('songs',views.songs,name='songs'),
    path('weather',views.weather,name='weather'),
    path('contactus',views.contactus,name='contactus'),
    path('scrapingCurrencies',views.scrapingCurrencies,name='scrapingCurrencies'),
    path('worldIndices',views.worldIndices,name='worldIndices'),
    path('commodities',views.commodities,name='commodities'),
    path('premierTable',views.premierTable,name='premierTable'),
    path('stock',views.stock,name='stock'),
    path('sports', views.sports, name='sports'),
    path('spanishTable',views.spanishTable,name='spanishTable'),
    path('italianTable',views.italianTable,name='italianTable'),
    path('f1', views.f1, name='f1')

]

