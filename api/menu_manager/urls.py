from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import apis

urlpatterns = [
    path('upload/', apis.MenuUploadApi.as_view(), name='upload'),
    path('total/', apis.OrdersAmountApi().as_view(), name='total'),
    path('menus/', apis.MenuFetchOrderApi().as_view(), name='order'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
