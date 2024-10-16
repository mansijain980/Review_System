from django.urls import path
from .views import ReviewScraperView

urlpatterns = [
     path('api/reviews', ReviewScraperView.as_view(), name='review-scraper'),
]
