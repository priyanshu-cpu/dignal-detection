# Django Signal Detection Assignment

This project implements the assignment as a local Django application.

It ingests public or sample RSS/HTML sources, extracts hiring and recruiting-related
signals with rule-based scoring, stores structured results in Django SQLite models,
and also exports JSON output for machine-readable downstream usage.

## Features

- Modular pipeline for fetching, parsing, scoring, and persistence
- Django dashboard for running detections and browsing results
- Django admin for inspecting runs and signals
- Signal modules under `signals/`
- Shared helpers under `utils/`
- Local JSON output plus Django SQLite database storage
- CLI runner and Django management command
- Optional serverless-style handler function
- Sample public-data fixtures for offline testing

## Project Structure

```text
config/
detector/
  models.py
  services.py
  views.py
  urls.py
  templates/detector/
signal_detection/
  parser.py
  storage.py
  signals/
  utils/
sample_data/
outputs/
manage.py
```

## Run

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and use the dashboard to trigger a detection run.

To run detection from the command line:

```bash
python manage.py run_detection
```

To pass explicit sources:

```bash
python manage.py run_detection --source sample_data/company_blog_rss.xml --source sample_data/news_feed_rss.xml
```

## Notes

- Uses only the Python standard library
- Django is the only framework dependency
- No paid APIs
- No LLM or external AI API usage
- Built to run locally
