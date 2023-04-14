from django.db import models


class AuthorOfQuote(models.Model):
    name = models.CharField(max_length=100, unique=True)
    born_date = models.CharField(max_length=100, blank=True, default='')
    born_location = models.CharField(max_length=100, blank=True, default='')
    description = models.TextField(max_length=300, blank=True, default='')

    def __str__(self):
        return self.name


class Quote(models.Model):
    text = models.TextField(max_length=300)
    author = models.ForeignKey(AuthorOfQuote, on_delete=models.CASCADE, related_name='quotes')

    def __str__(self):
        return self.text
