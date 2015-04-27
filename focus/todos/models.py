from django.db import models


class Todo(models.Model):
    text = models.CharField(max_length=200)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.text
