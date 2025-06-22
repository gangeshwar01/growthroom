from django.contrib import admin
from .models import TrainingSession, TrainingAttendance

@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'date', 'time', 'get_assigned_employees_count')
    list_filter = ('date', 'topic', 'assigned_employees')
    search_fields = ('title', 'topic', 'description')
    filter_horizontal = ('assigned_employees',)
    
    def get_assigned_employees_count(self, obj):
        return obj.assigned_employees.count()
    get_assigned_employees_count.short_description = 'Assigned Employees'

@admin.register(TrainingAttendance)
class TrainingAttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'attended', 'created_at')
    list_filter = ('attended', 'session', 'user')
    search_fields = ('user__username', 'session__title')
