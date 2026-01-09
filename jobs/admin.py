from django.contrib import admin
from .models import Job

# Register your models here.

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary', 'created_at')
    search_fields = ('title', 'company', 'location')
    list_filter = ('company', 'location')