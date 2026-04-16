from __future__ import annotations

from django.contrib import admin

from detector.models import DetectionRun, SignalRecord


@admin.register(DetectionRun)
class DetectionRunAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "source_count", "signal_count", "notes")
    search_fields = ("notes",)
    readonly_fields = ("created_at",)


@admin.register(SignalRecord)
class SignalRecordAdmin(admin.ModelAdmin):
    list_display = ("company", "signal_type", "signal_score", "detected_at", "run")
    list_filter = ("signal_type", "run")
    search_fields = ("company", "title", "reason", "source_url")
    readonly_fields = ("created_at",)
