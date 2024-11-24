from django.db import models

class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    ]
    
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='available'
    )
    
    def __str__(self):
        return self.title

    def borrow(self):
        self.status = 'borrowed'
        self.save()

    def return_book(self):
        self.status = 'available'
        self.save()
