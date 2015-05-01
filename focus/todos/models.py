from django.db import models


class Todo(models.Model):
    text = models.CharField(
        default='New Todo',
        max_length=200
    )
    priority = models.IntegerField(
        null=True,
        blank=True
    )
    complete = models.BooleanField(default=False)

    @property
    def next(self):
        """Return the next highest priority todo."""
        return Todo.objects.order_by('priority').filter(
            priority__gt=self.priority
        ).first()

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        """
        Override the default save to push objects with the same priority
        down.
        """
        if self.priority:
            todo = Todo.objects.filter(priority=self.priority).first()
            if todo:
                todo.priority += 1
                todo.save()
        else:
            self.priority = Todo.objects.count() + 1

        super(Todo, self).save(*args, **kwargs)
