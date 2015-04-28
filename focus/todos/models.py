from django.db import models


class Todo(models.Model):
    text = models.CharField(max_length=200)
    priority = models.IntegerField(unique=True)
    complete = models.BooleanField(default=False)

    @property
    def next(self):
        """Return the next highest priority todo"""
        return Todo.objects.order_by('priority').filter(
            priority__gt=self.priority
        ).first()

    def __str__(self):
        return self.text
