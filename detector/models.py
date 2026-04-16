from __future__ import annotations

from django.db import models


class DetectionRun(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    source_count = models.PositiveIntegerField(default=0)
    signal_count = models.PositiveIntegerField(default=0)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Run {self.pk} ({self.signal_count} signals)"


class SignalRecord(models.Model):
    SIGNAL_TYPES = [
        ("mass_hiring", "Mass hiring"),
        ("hiring_activity", "Hiring activity"),
        ("recruiting_signal", "Recruiting signal"),
    ]

    run = models.ForeignKey(
        DetectionRun,
        on_delete=models.CASCADE,
        related_name="signals",
    )
    company = models.CharField(max_length=255)
    signal_type = models.CharField(max_length=50, choices=SIGNAL_TYPES)
    source_url = models.URLField(max_length=500)
    matched_keywords = models.JSONField(default=list)
    signal_score = models.PositiveIntegerField()
    detected_at = models.DateTimeField()
    reason = models.TextField()
    title = models.CharField(max_length=500)
    published_at = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-signal_score", "-detected_at"]

    def __str__(self) -> str:
        return f"{self.company} - {self.signal_type} ({self.signal_score})"
