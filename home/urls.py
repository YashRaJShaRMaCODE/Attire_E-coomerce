
from django.contrib import admin
from django.urls import path,include
from home import views


urlpatterns = [
   path("",views.index,name='home'),
   path("about/",views.about,name='about' ),
   path("services/",views.services,name='services'),
   path("contact/",views.contact,name='contact'),
   path("feedback/",views.feedback,name='feedback'),
   path('profile-settings/', views.profile_settings, name='profile_settings'),
   path('account-settings/', views.account_settings, name='account_settings'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('my-account/', views.my_account, name='my_account'),
    path('my-account/settings/profile-setting/', views.profile_setting, name='profile_setting'),
    path('my-account/settings/account-setting/', views.account_setting, name='account_setting'),
    path('my-account/my-orders/', views.my_orders, name='my_orders'),
    path('my-account/settings/saved-addresses/', views.saved_addresses, name='saved_addresses'),
    path('settings/', views.settings, name='settings'),
    path("purchase-history/",views.purchase_history,name='purchase_history')
    ]
