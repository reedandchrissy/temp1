from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
	#Leave as empty string for base url
    path('login/', views.loginpage, name="login"),
    path('logout/', views.logoutuser, name="logout"),
    path('register/', views.register, name="register"),
    path('', views.home, name="home"),
	path('homein/', views.homein, name="homein"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('comments/', views.comments, name="comments"),
    path('commentsin/', views.commentsin, name="commentsin"),
    path('store/', views.store, name="store"),
    path('storein/', views.storein, name="storein"),
    path('contact/', views.contact, name="contact"),
    path('contactin/', views.contactin, name="contactin"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('reports/', views.reports, name="reports"),
    path('delivery/', views.delivery, name="delivery"),
    path('customer_info/', views.customerInfo, name="customer_info"),

    path('updateorder/<str:pk>/', views.updateorder, name='updateorder'),
    path('deleteorder/<str:pk>/', views.deleteorder, name='deleteorder'),
    path('status/<str:pk>/', views.status, name='status'),

    path('customer/', views.userpage, name='customer'),
    path('write_comment/', views.writeComment, name='write_comment'),
    path('customer_setting/', views.customersetting, name='customer_setting'),
    path('ReturnManagement/', views.Return, name='ReturnManagement'),
    path('enter_return_item/', views.enterItem, name='enter_return_item'),

    path('order/<str:pk_test>/', views.order, name='order'),
    path('receipt/<str:pk_test>/', views.receipt, name='receipt'),

    path('website_report/<str:pk>/', views.websiteReport, name='website_report'),
    path('farm_report/<str:pk>/', views.farmReport, name='farm_report'),
    path('overall_report/<str:pk>/', views.overallReport, name='overall_report'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="store/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="store/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="store/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="store/password_reset_done.html"),
         name="password_reset_complete"),
]
