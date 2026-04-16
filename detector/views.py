from __future__ import annotations

from django.contrib import messages
from django.db.models import Avg, Count, Max
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from detector.models import DetectionRun, SignalRecord
from detector.services import DEFAULT_SOURCES, run_detection


@require_GET
def dashboard(request: HttpRequest) -> HttpResponse:
    signals = SignalRecord.objects.select_related("run").all()[:25]
    runs = DetectionRun.objects.annotate(signal_total=Count("signals"))[:10]
    stats = SignalRecord.objects.aggregate(
        total=Count("id"),
        companies=Count("company", distinct=True),
        avg_score=Avg("signal_score"),
        top_score=Max("signal_score"),
    )
    context = {
        "signals": signals,
        "runs": runs,
        "stats": stats,
        "default_sources": DEFAULT_SOURCES,
    }
    return render(request, "detector/dashboard.html", context)


@require_POST
def run_detection_view(request: HttpRequest) -> HttpResponse:
    raw_sources = request.POST.get("sources", "").strip()
    sources = [line.strip() for line in raw_sources.splitlines() if line.strip()]
    run = run_detection(sources or None)
    messages.success(
        request,
        f"Detection finished. Processed {run.source_count} sources and stored {run.signal_count} signals.",
    )
    return redirect("detector:dashboard")


@require_GET
def run_detail(request: HttpRequest, run_id: int) -> HttpResponse:
    run = get_object_or_404(DetectionRun.objects.prefetch_related("signals"), pk=run_id)
    return render(request, "detector/run_detail.html", {"run": run})

