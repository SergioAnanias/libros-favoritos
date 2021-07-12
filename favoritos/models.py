from django.db import models
from app.models import User
# Create your models here.

class BookManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData['title']) < 2:
            errors['title']="El nombre no es valido"
        if len(Book.objects.filter(title=postData['title'])) > 0:
            errors['title2']= "El libro ya existe"
        if len(postData['desc']) < 5:
            errors['description']="La descripción es muy corta"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name='books', null=True, on_delete=models.SET_NULL)
    liked_by = models.ManyToManyField(User, related_name='liked_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= BookManager()