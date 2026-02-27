from django.contrib import admin

from .models import LiveConfig, Notice


@admin.register(LiveConfig)
class LiveConfigAdmin(admin.ModelAdmin):
    list_display = ("subject", "live_url", "updated_at")
    list_filter = ("subject",)
    search_fields = ("live_url",)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ("subject", "short_message", "created_at", "is_active")
    list_filter = ("subject", "is_active")
    search_fields = ("message",)

    def short_message(self, obj):
        return (obj.message[:60] + "...") if len(obj.message) > 60 else obj.message

