from django.db import models

class Review(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    rating = models.IntegerField()
    reviewer = models.CharField(max_length=255)
    product_url = models.URLField()

    def __str__(self):
        return self.title