from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import apis

urlpatterns = [
    path('upload/', apis.MenuUploadApi.as_view()),
    path('total/', apis.OrdersAmountApi().as_view()),
    path('menus/', apis.MenuFetchOrderApi().as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
