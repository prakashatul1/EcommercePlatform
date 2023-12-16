from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from deal import views

urlpatterns = [
    path('deals', views.DealList.as_view()),
    path('deals/<int:pk>', views.DealDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
