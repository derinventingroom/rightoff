from django.db import models


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('Software', 'Software'),
        ('Equipment', 'Equipment'),
        ('Internet', 'Internet'),
        ('Office Supplies', 'Office Supplies'),
        ('Mileage', 'Mileage'),
        ('Advertising', 'Advertising'),
        ('Education', 'Education'),
        ('Travel', 'Travel'),
        ('Other', 'Other'),
    ]

    date = models.DateField()

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    description = models.CharField(max_length=255)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return self.description