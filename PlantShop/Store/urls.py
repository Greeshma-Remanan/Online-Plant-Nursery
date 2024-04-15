from django.urls import path
from Store import views

urlpatterns=[
    path('',views.Home.as_view(),name='home'),
    path('product/<int:pk>',views.ProductView.as_view(),name='product'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.logoutView.as_view(),name='logout'),
    path('product_details/<int:pk>',views.ProductDetail.as_view(),name='prod_det'),
    path('cart_details/',views.CartDetail.as_view(),name='cart_detail'),
    path('cart/<int:pk>',views.Addtocart.as_view(),name='cart'),
    path('delete_cart/<int:pk>',views.CartDelete.as_view(),name='cart_delete'),
    path('order/<int:pk>',views.OrderView.as_view(),name='order'),
    path("remove_order/<int:pk>",views.remove_order.as_view(),name='remove_order'),
    path('search/all',views.SearchView.as_view(),name='srch'),
    path('pay/',views.OrderView.as_view(),name='pay'),
     path('orders/', views.OrderListView.as_view(), name='order_list'),
   
]