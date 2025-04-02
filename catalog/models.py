from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Author(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Work(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author, related_name='works')
    publication_year = models.IntegerField()
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class Loan(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='loans')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    loan_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    returned_date = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Set due date to 2 weeks after loan date if not already set
        if not self.due_date:
            self.due_date = self.loan_date + timedelta(weeks=2)
        
        # Update work availability
        if self.returned_date:
            self.work.available = True
        else:
            self.work.available = False
        self.work.save()
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.work.title} - {self.user.username}"