from django.contrib import admin

from todos.models import Todo


class TodoAdmin(admin.ModelAdmin):
    fields = ['text', 'priority']
    list_display = ('text', 'priority')
    ordering = ('priority',)

admin.site.register(Todo, TodoAdmin)
