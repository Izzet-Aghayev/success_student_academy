# SUCCESS STUDENT ACADEMY - Product Requirements Document

## Overview
- **Summary**: A complete Django (MVT) promotional and enrollment website for SUCCESS STUDENT ACADEMY, featuring a premium 6-breakpoint responsive UI, Student Registration form, and Feedback form — both forms persist to the database AND deliver submissions simultaneously via Telegram Bot and SMTP Email.
- **Purpose**: Provide the academy with a modern, fast, mobile-first web presence that converts visitors into registered students and collects actionable feedback, with instant multi-channel notifications to the academy staff.
- **Target Users**: Prospective students (and their parents), current students, academy administrators/staff, and general visitors researching the academy.

## Goals
- A production-ready Django project skeleton with correct MVT separation (models, views, forms, urls, templates, static).
- 6-breakpoint responsive UI (Bootstrap 5 xs/sm/md/lg/xl/xxl) using glassmorphism, deep-blue #1e3a8a palette, subtle gradients, 3D effects.
- Two working forms (Registration + Feedback) validated on both client and server, with:
  - Database persistence (MySQL-ready models)
  - Telegram Bot notification (background thread)
  - SMTP Email notification (background thread)
- Namespaced URLs (`core:home`, `core:registration`, `core:feedback`, etc.)
- HTMX included for SPA-like partial-page navigation feel.
- `.env.example` and `requirements.txt` suitable for local + production deployment.

## Non-Goals
- No user authentication / RBAC dashboard (out of scope for this setup).
- No payment / checkout integration.
- No CMS or course LMS features beyond listing courses.
- No live testing against real Telegram/Email credentials (only code paths + env wiring).
- No Docker / CI files unless specifically requested.

## Background & Context
- User profile preferences: Django MVT, MySQL, Bootstrap 5, glassmorphism, #1e3a8a deep blue, namespaced URLs, HTMX, `threading.Thread(daemon=True)` for lightweight background notification tasks with explicit DB cleanup.
- Project directory starts empty (greenfield).

## Functional Requirements

- **FR-1 (Project Layout)**: Django project named `config` with single app `core`; standard MVT directories (`models.py`, `views.py`, `forms.py`, `urls.py`, `admin.py`); project-level `static/`, `templates/`, `media/`; `manage.py` at repo root.
- **FR-2 (Settings)**: `settings.py` uses `python-dotenv` to source DB, Email, Telegram, SECRET_KEY from `.env`; `INSTALLED_APPS` includes `core`; `TEMPLATES` resolves project-level `templates/`; `STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIRS` wired; `MEDIA_URL`/`MEDIA_ROOT` wired; `DEFAULT_AUTO_FIELD = BigAutoField`; namespaced URL inclusion.
- **FR-3 (Registration Model & Form)**: Model `StudentRegistration` with fields: `full_name`, `email`, `phone`, `date_of_birth`, `gender` (choices: Male/Female/Other), `address`, `selected_course` (choices), `education_level` (choices), `parent_name`, `parent_phone`, `additional_notes` (optional text), `created_at`; `forms.ModelForm` with appropriate widgets, labels, help_text and validators (email format, phone format, required fields).
- **FR-4 (Feedback Model & Form)**: Model `Feedback` with fields: `full_name`, `email`, `subject`, `rating` (1-5 integer), `message`, `is_student` (bool), `course_taken` (char, optional), `created_at`; `forms.ModelForm` with widgets and validators.
- **FR-5 (Telegram Notifications)**: Utility `send_telegram_message(token, chat_id, text)` — HTTPS POST to Telegram Bot API `sendMessage`; called inside a `threading.Thread(daemon=True)` that closes DB connections via `django.db.connections.close_all()` on completion. Registration and Feedback submissions each send a formatted Telegram message.
- **FR-6 (Email Notifications)**: Utility `send_email_notification(subject, plain_message, html_message, from_email, recipient_list)` using Django `send_mail`; wrapped in the same daemon-thread + `close_all()` pattern. Both forms trigger templated HTML+PLAIN email.
- **FR-7 (Views & URLs)**: Views render templates and handle form POST with success-redirect + flash message (`django.contrib.messages`). URL namespaces: `core:home`, `core:about`, `core:courses`, `core:course_detail`, `core:teachers`, `core:gallery`, `core:contact`, `core:registration`, `core:feedback`. Named URLs used exclusively in templates.
- **FR-8 (Admin)**: Both models registered on Django Admin with `list_display`, `list_filter`, `search_fields`, `readonly_fields = ("created_at",)`.
- **FR-9 (Templates)**: Project-level `templates/base.html` (skeleton, navbar, messages, footer, asset blocks); then `templates/core/home.html`, `about.html`, `courses.html`, `course_detail.html`, `teachers.html`, `gallery.html`, `contact.html`, `registration.html`, `feedback.html`. Partials/includes for navbar/footer encouraged.
- **FR-10 (Static Assets)**: `static/css/main.css` (Bootstrap 5 CDN + custom overrides implementing glassmorphism, #1e3a8a theme, 6-breakpoint responsive classes, subtle gradient backgrounds, 3D hover transforms); `static/js/main.js` (HTMX init, form UX helpers, navbar interactions); any static images referenced from templates use the allowed `coresg-normal.trae.ai` image URL.
- **FR-11 (6-Breakpoint UI)**: Layout explicitly designed across Bootstrap's 6 tiers — `xs (<576px)`, `sm (≥576)`, `md (≥768)`, `lg (≥992)`, `xl (≥1200)`, `xxl (≥1400)`. Evidence: hero grid columns, card row gutters, navbar collapse behavior, font-size scaling, container widths all use appropriate `-sm-`, `-md-`, `-lg-`, `-xl-`, `-xxl-` modifiers and matching media queries in CSS.
- **FR-12 (Environment)**: `.env.example` documents all required variables (SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_*, EMAIL_*, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, CONTACT_EMAIL_RECIPIENT). `requirements.txt` pinned packages: Django 5.x, mysqlclient, python-dotenv, requests, crispy-bootstrap5, django-crispy-forms, whitenoise.

## Non-Functional Requirements
- **NFR-1 (Security)**: CSRF tokens on every form; `{% csrf_token %}` present; no hardcoded credentials ever; settings sourced from env.
- **NFR-2 (Performance)**: Notifications dispatched via daemon thread so HTTP response does not block on external APIs (SMTP/Telegram latency).
- **NFR-3 (Portability)**: DB backend configurable via `.env` (MySQL primary, SQLite fallback for quick local dev).
- **NFR-4 (Maintainability)**: Namespaced URL pattern usage everywhere; consistent Django naming conventions.

## Constraints
- **Technical**: Django MVT (no DRF views required unless needed for AJAX; HTMX partial endpoints OK). Bootstrap 5 (CDN). MySQL as primary target. No comments in code unless requested explicitly.
- **Business**: Brand is "SUCCESS STUDENT ACADEMY". Primary color `#1e3a8a` (deep blue). Glassmorphism aesthetic for hero cards, navbars, modals.
- **Dependencies**: Telegram Bot API requires user-provided token/chat_id via `.env`. SMTP requires user-provided credentials. No keys committed.

## Assumptions
- `selected_course` choices populated with reasonable academy offerings (e.g., SAT Prep, IELTS, TOEFL, Math, Physics, Chemistry, Biology, Turkish, English, Coding, Robotics).
- `education_level` choices: Middle School, High School (9/10/11/12), University Prep, Graduate.
- Gallery and Teachers pages use static placeholder data in templates (no models).
- Course list/detail uses a static COURSES list (in views) for now; model-backed courses can be added later without breaking templates.

## Acceptance Criteria

### AC-1: Django project compiles and serves pages
- **Type**: `rule`
- **Given**: A clean clone with `.env` populated from `.env.example` and `pip install -r requirements.txt` run
- **When**: `python manage.py check` is executed and `python manage.py runserver` starts
- **Then**: `check` returns exit code 0; the dev server listens and responds HTTP 200 for `/`, `/registration/`, `/feedback/`, `/about/`, `/courses/`, `/teachers/`, `/gallery/`, `/contact/`
- **Pass Condition**: `python manage.py check` == 0 AND smoke-test GET URLs return 200
- **Evidence**: Terminal output of `check` command + curl or browser 200s

### AC-2: Models migrate cleanly on SQLite (quick) and MySQL (configured)
- **Type**: `rule`
- **Given**: Fresh DB state
- **When**: `python manage.py makemigrations core` then `python manage.py migrate`
- **Then**: Both commands exit 0; tables `core_studentregistration` and `core_feedback` exist
- **Pass Condition**: makemigrations + migrate exit codes == 0; sqlmigrate output shows correct columns
- **Evidence**: Command output captured

### AC-3: Registration form saves to DB AND triggers Telegram + Email
- **Type**: `rule`
- **Given**: `.env` has `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `EMAIL_*`, and `CONTACT_EMAIL_RECIPIENT` set (even with placeholders)
- **When**: A valid POST is submitted to `core:registration`
- **Then**: One `StudentRegistration` row is created; a daemon thread starts `send_telegram_message`; a daemon thread starts `send_email_notification`; response is 302 redirect with success message
- **Pass Condition**: DB record present + code-path inspection confirms both notifiers invoked on valid POST
- **Evidence**: Query `StudentRegistration.objects.count()`, inspect view body for thread invocations

### AC-4: Feedback form saves to DB AND triggers Telegram + Email
- **Type**: `rule`
- **Same logic as AC-3 but against Feedback model/route
- **Pass Condition**: Analogous
- **Evidence**: Analogous

### AC-5: Namespaced URLs used exclusively in templates and views
- **Type**: `rule`
- **Given**: Entire repo
- **When**: Grep templates and `views.py` for URL references
- **Then**: Every `<a href>` form action and `reverse()` call uses `{% url 'core:name' %}` or `reverse('core:name')`; no hardcoded `/registration/` path strings
- **Pass Condition**: Zero matches of hardcoded paths (except `LOGIN_URL` style settings constants if any)
- **Evidence**: Grep result

### AC-6: 6-breakpoint responsive layout visually adapts across all 6 Bootstrap tiers
- **Type**: `rubric`
- **Dimension**: Responsive UI fidelity across 6 breakpoints
- **Scale**: 1-5
- **Anchors**: 1 = mobile only, no breakpoints used; 3 = md/lg covered but xs/sm/xl/xxl missing modifiers; 5 = every section (hero, cards, nav, footer, typography) uses appropriate `-sm-`, `-md-`, `-lg-`, `-xl-`, `-xxl-` Bootstrap classes AND CSS media query overrides exist for each tier where Bootstrap utilities do not cover it
- **Pass Threshold**: >= 4
- **Evidence**: Inspection of `main.css` media queries and template Bootstrap class usage

### AC-7: Premium glassmorphism UI aesthetic with deep blue palette
- **Type**: `rubric`
- **Dimension**: Visual quality / brand match
- **Scale**: 1-5
- **Anchors**: 1 = plain Bootstrap default; 3 = custom color but no glassmorphism; 5 = navbar/hero cards use `backdrop-filter: blur()`, semi-transparent white, layered shadows; #1e3a8a used for primary buttons/gradients/accents; subtle 3D hover on cards
- **Pass Threshold**: >= 4
- **Evidence**: `main.css` contents and template class assignments

### AC-8: Notifications do not block HTTP response
- **Type**: `rule`
- **Given**: Valid form submit
- **When**: Time the POST response
- **Then**: The code path wraps each notifier in `threading.Thread(daemon=True).start()` before returning the response; view does not `join()`
- **Pass Condition**: Source review confirms both notifier calls happen inside started daemon threads with no join
- **Evidence**: Views/notifier code inspection

### AC-9: `.env.example` and `requirements.txt` present and complete
- **Type**: `rule`
- **Given**: Repo root
- **When**: Files exist
- **Then**: `.env.example` defines SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_ENGINE/NAME/USER/PASSWORD/HOST/PORT, EMAIL_BACKEND/HOST/PORT/USE_TLS/HOST_USER/HOST_PASSWORD/DEFAULT_FROM_EMAIL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, CONTACT_EMAIL_RECIPIENT; `requirements.txt` lists at least Django, mysqlclient, python-dotenv, requests, django-crispy-forms, crispy-bootstrap5, whitenoise
- **Pass Condition**: Grep confirms each key above is present in the respective file
- **Evidence**: File contents

## Open Questions
- [ ] None currently — using standard/recommended defaults from user profile preferences.
