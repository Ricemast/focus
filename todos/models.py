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
    def previous(self):
        """Return the id of the previous highest priority todo."""
        t = Todo.objects.order_by('priority').filter(
            priority__lt=self.priority
        ).last()
        return t.id if t else None

    @property
    def next(self):
        """
        Return the id of the next highest priority todo which is not
        complete.
        """
        t = Todo.objects.order_by('priority').filter(
            priority__gt=self.priority,
            complete=False
        ).first()
        return t.id if t else None

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        """
        Override the default save to push objects with the same priority
        down.
        """
        if not self.priority:
            if Todo.objects.count() > 0:
                self.priority = Todo.objects.aggregate(
                    models.Max('priority')
                )['priority__max'] + 1
            else:
                self.priority = 1

        super(Todo, self).save(*args, **kwargs)
