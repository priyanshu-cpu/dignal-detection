from __future__ import annotations

from django.test import Client, TestCase
from django.urls import reverse

from detector.models import DetectionRun, SignalRecord
from detector.services import run_detection


class DetectorTests(TestCase):
    def test_run_detection_creates_records(self) -> None:
        run_count_before = DetectionRun.objects.count()
        signal_count_before = SignalRecord.objects.count()
        run = run_detection()

        self.assertEqual(run.source_count, 2)
        self.assertGreaterEqual(run.signal_count, 1)
        self.assertEqual(DetectionRun.objects.count(), run_count_before + 1)
        self.assertEqual(SignalRecord.objects.count(), signal_count_before + run.signal_count)

    def test_dashboard_renders(self) -> None:
        client = Client()
        response = client.get(reverse("detector:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Signal Detection Dashboard")
