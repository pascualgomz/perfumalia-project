from django.urls import path
from .views import *
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.i18n import set_language

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("", HomePageView.as_view(), name='home'),
    path("user", ProfilePageView.as_view(), name='profile'),
    path("perfumes", PerfumesPageView.as_view(), name='perfumes'),
    path("perfumes/<int:pk>/", PerfumesDetailsPageView.as_view(), name='perfumedetails'),
    path("cart", CartPageView.as_view(), name='cart'),
    path("order", OrdersPageView.as_view(), name='orders'),
    path("order/<int:pk>/", OrderDetailsPageView.as_view(), name='orderdetails'),
    path("user", ProfilePageView.as_view(), name='profile'),
    path("search/<str:query>/", SearchResultsPageView.as_view(), name='searchresults'),
    path('logout/', LogoutView, name='logout'),
    path('logout-success/', LogoutSuccessView, name='logout_success'),
    path('add-to-cart/<str:productID>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:productID>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('complete-order/', CompleteOrderView.as_view(), name='complete_order'),
    path('payment/', PaymentPageView.as_view(), name='payment'),
    path('subscriptions/', SubscriptionsPageView.as_view(), name='subscriptions'),
    path('subscriptions/<int:pk>/', SubscriptionDetailsPageView.as_view(), name='subscriptiondetails'),
    path('subscribe/<int:planID>/', SubscribeView.as_view(), name='subscribe'),
    path('subscriptionplans/', SubscriptionPlansPageView.as_view(), name='subscription_plans'),
    path('cancelsubscription/<int:pk>/', CancelSubscriptionView.as_view(), name='cancel_subscription'),
    path("news", NewsPageView.as_view(), name='news'),
    path('generar_pdf/', generar_cheque_pdf, name='generar_pdf'),
    path('generar_html/', generar_cheque_html, name='generar_html'),
    path("hotwheels", HotWheelsPageView.as_view(), name='hotwheels'),
    path('set_language/', set_language, name='set_language'),
]