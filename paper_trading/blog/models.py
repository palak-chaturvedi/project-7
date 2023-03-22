from django.db import models

# Create your models here.


class Articles(models.Model):
    Author = models.CharField(max_length=50, null=False)
    Title = models.CharField(max_length=50)
    Description = models.TextField(max_length=300)
    ArticleImage = models.ImageField(upload_to="ArticleImage/")
    active = models.BooleanField(default=True, null=True)
    Date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Author + " " + self.Title
