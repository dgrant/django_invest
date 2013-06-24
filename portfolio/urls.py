from django.conf.urls import url, patterns
from django.views.generic import ListView
from portfolio.views import HoldingCreate

urlpatterns = patterns('',
     url(r'^holdings/$', 'portfolio.views.HoldingList', name='holdings_list'),
     url(r'^holding/create/$', HoldingCreate.as_view(), name='holding_create'),
     url(r'^holding/(\d+)/$', 'portfolio.views.HoldingDetail', name='holding_detail'),
     url(r'^holding/(\d+)/delete/$', 'portfolio.views.holding_delete', name='holding_delete'),
)
