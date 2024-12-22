from django.db import models

# Create your models here.
class KnapsackProblem(models.Model):
    capacity = models.IntegerField()
    profits = models.TextField()  # Stocker les profits comme une liste JSON
    weights = models.TextField()  # Stocker les poids comme une liste JSON