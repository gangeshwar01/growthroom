from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'status', 'check_in', 'check_out')
    list_filter = ('user', 'status', 'date')
    search_fields = ('user__username', 'user__id', 'user__email')
