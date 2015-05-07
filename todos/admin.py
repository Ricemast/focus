from django.contrib import admin

from todos.models import Todo


class TodoAdmin(admin.ModelAdmin):
    fields = ['text', 'complete']
    list_display = ('text', 'priority', 'complete')
    ordering = ('priority',)

admin.site.register(Todo, TodoAdmin)
