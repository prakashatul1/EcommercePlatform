from django.urls import path
from deal import views

urlpatterns = [
    path('deals', views.deal_list),
    path('deals/<int:pk>', views.deal_detail)
]