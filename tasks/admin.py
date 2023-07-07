from django.contrib import admin
from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin): #asi agregamos campos de solos lectura
	readonly_fields = ("created_at",)

admin.site.register(Task, TaskAdmin)