# SUCCESS STUDENT ACADEMY - Implementation Plan

## Task 1: Scaffold Django project skeleton (config package, manage.py)
- **Status**: `pending`
- **Priority**: high
- **Depends On**: None
- **Description**:
  - Create repo-root `manage.py` entry script
  - Create `config/` package: `__init__.py`, `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`
  - `settings.py`: dotenv loading, BASE_DIR, SECRET_KEY/DEBUG from env, ALLOWED_HOSTS, INSTALLED_APPS with `core`, MIDDLEWARE with Whitenoise, TEMPLATES pointing at `templates/`, DATABASES env-driven (MySQL primary, SQLite fallback), STATIC_URL/ROOT/FILES_DIRS, MEDIA_URL/ROOT, MESSAGES, CRISPY_ALLOWED_TEMPLATE_PACKS/bootstrap5, DEFAULT_AUTO_FIELD, EMAIL settings from env, TELEGRAM settings from env
  - `config/urls.py`: includes `core.urls` with `app_name='core'` namespace
- **Acceptance Criteria Addressed**: AC-1, AC-9
- **Test Requirements**:
  - `rule` TR-1.1: `python manage.py check` returns exit code 0
  - `rule` TR-1.2: `settings.py` imports and parses dotenv; TELEGRAM + EMAIL + DB keys read via `os.getenv`
  - `rule` TR-1.3: `config/urls.py` uses `include(('core.urls', 'core'), namespace='core')` or `app_name` in core.urls

## Task 2: Create `core` app (models, forms, admin, urls, views, apps)
- **Status**: `pending`
- **Priority**: high
- **Depends On**: Task 1
- **Description**:
  - `core/__init__.py`, `apps.py` with `CoreConfig`
  - `core/models.py`: `StudentRegistration` (fields per FR-3) and `Feedback` (fields per FR-4); proper `__str__`, ordering by `-created_at`
  - `core/forms.py`: `StudentRegistrationForm(ModelForm)`, `FeedbackForm(ModelForm)`; widgets (SelectDateWidget, Select, Textarea, EmailInput, TelInput, NumberInput); validators for email, phone regex, rating min/max
  - `core/admin.py`: register both models with custom list_display, list_filter, search_fields, readonly_fields=('created_at',)
  - `core/urls.py`: set `app_name = 'core'`; 9 patterns mapped to views (home, about, courses, course_detail, teachers, gallery, contact, registration, feedback)
  - `core/views.py`: all 9 views; registration and feedback handle POST, form_valid saves, triggers both notifiers via threads, redirects with `messages.success`; invalid forms re-render with errors; GET requests render templates with any required context (COURSES list, TEACHERS list, GALLERY items)
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3, AC-4, AC-5
- **Test Requirements**:
  - `rule` TR-2.1: `makemigrations core` produces a non-empty migration file with both models
  - `rule` TR-2.2: view code only uses `reverse('core:name')` and templates only use `{% url 'core:name' %}`
  - `rule` TR-2.3: forms define explicit `fields`/`exclude`, widgets, clean methods where required (rating 1-5, phone regex)
  - `rule` TR-2.4: admin class includes `list_display`, `list_filter`, `search_fields` for both models

## Task 3: Notification utilities (Telegram + Email via daemon threads)
- **Status**: `pending`
- **Priority**: high
- **Depends On**: Task 1, Task 2
- **Description**:
  - `core/utils.py` module
  - `send_telegram_message(token, chat_id, text)` using `requests.post` to `https://api.telegram.org/bot{token}/sendMessage` with JSON body; catches and logs exceptions (no crash propagation)
  - `send_email_notification(subject, plain_message, html_message, from_email, recipient_list)` using `django.core.mail.send_mail` with `html_message` kwarg
  - `notify_registration_submission(instance)` — formats Telegram text and email body; starts 2 daemon threads
  - `notify_feedback_submission(instance)` — same
  - Every thread target closes DB connections via `django.db.connections.close_all()` at the end
- **Acceptance Criteria Addressed**: AC-3, AC-4, AC-8
- **Test Requirements**:
  - `rule` TR-3.1: Both notify functions call `threading.Thread(target=..., daemon=True).start()` exactly twice each, without `.join()`
  - `rule` TR-3.2: Thread target function body calls `close_all()` after network call / send_mail
  - `rule` TR-3.3: Telegram URL construction correct; payload includes `chat_id` and `text`; email calls `send_mail(html_message=...)`

## Task 4: requirements.txt + .env.example
- **Status**: `pending`
- **Priority**: high
- **Depends On**: None
- **Description**:
  - `requirements.txt` pinned: `Django>=5.0,<5.2`, `mysqlclient>=2.2`, `python-dotenv>=1.0`, `requests>=2.31`, `django-crispy-forms>=2.1`, `crispy-bootstrap5>=2024.2`, `whitenoise>=6.6`
  - `.env.example`: all keys from FR-12 with sensible default placeholders; MySQL example + SQLite option commented; email SMTP example
- **Acceptance Criteria Addressed**: AC-9
- **Test Requirements**:
  - `rule` TR-4.1: All 7 package names appear in requirements.txt
  - `rule` TR-4.2: All env keys from AC-9 pass condition exist in `.env.example`

## Task 5: Static CSS + JS (6-breakpoint, glassmorphism, HTMX)
- **Status**: `pending`
- **Priority**: high
- **Depends On**: None
- **Description**:
  - `static/css/main.css`: custom Bootstrap 5 overrides; `:root` CSS vars for `--primary: #1e3a8a` and family; `.glass` (backdrop-filter: blur(18px); bg rgba(255,255,255,0.12); border rgba(255,255,255,0.2); shadow); gradient bg utility `.bg-gradient-deep` (linear-gradient 135deg #1e3a8a -> #3b82f6 -> #0f172a); card hover 3D transform `translateY(-4px) rotateX(2deg)` + shadow transition; responsive typography `.rfs-*`-style scaling; media query blocks for each of 6 tiers adjusting hero heading, card columns, nav padding, container max-width overrides
  - `static/js/main.js`: navbar scroll glass toggling; form loading/disabled state on submit; optional HTMX configuration (`htmx.config.useTemplateFragments = true`); smooth scroll
- **Acceptance Criteria Addressed**: AC-6, AC-7
- **Test Requirements**:
  - `rule` TR-5.1: CSS file includes explicit `@media (min-width: 576px)`, `@media (min-width: 768px)`, `@media (min-width: 992px)`, `@media (min-width: 1200px)`, `@media (min-width: 1400px)` blocks (xs covered by defaults, 5 explicit media queries = 6 tiers)
  - `rubric` TR-5.2: Glassmorphism + palette fidelity; scale 1-5; 1 = none, 3 = colors only, 5 = `.glass` class with backdrop-filter/blur/shadow/border, `.bg-gradient-deep` uses #1e3a8a, primary buttons use .btn-primary with #1e3a8a override, 3D card hover; threshold >= 4; evidence = main.css
  - `rule` TR-5.3: main.js references HTMX config or integrates HTMX event handlers; CDN include in base

## Task 6: Templates (base + 9 page templates + partials)
- **Status**: `pending`
- **Priority**: high
- **Depends On**: Task 1, Task 2, Task 5
- **Description**:
  - `templates/base.html`: `{% load static %}`, Bootstrap 5 CSS CDN, `main.css`, HTMX CDN, custom `{% block content %}`, navbar with links using `{% url 'core:...' %}`, `{% include 'partials/messages.html' %}`, footer, Bootstrap 5 JS bundle, `main.js`
  - `templates/partials/_navbar.html` (glassmorphism navbar, brand SUCCESS STUDENT ACADEMY, mobile toggle)
  - `templates/partials/_footer.html`
  - `templates/partials/_messages.html` (Django messages styled as Bootstrap alerts)
  - `templates/core/home.html`: hero (glass card with CTA buttons to registration/contact), features row, stats section, testimonials, CTA band
  - `templates/core/about.html`: about sections, vision mission values, why choose us
  - `templates/core/courses.html`: course cards grid (6-breakpoint column classes `col-sm-6 col-md-6 col-lg-4 col-xl-4 col-xxl-3` pattern)
  - `templates/core/course_detail.html`: static course detail (slug-driven context)
  - `templates/core/teachers.html`: teacher profile cards grid
  - `templates/core/gallery.html`: responsive photo gallery (masonry/grid) using placeholder image URLs from coresg-normal.trae.ai as spec allows
  - `templates/core/contact.html`: contact info + iframe-less map placeholder + note that registration/feedback forms exist on dedicated pages
  - `templates/core/registration.html`: crispy-rendered `StudentRegistrationForm`, POST to `{% url 'core:registration' %}`, `{% csrf_token %}`, submit button, success flash area
  - `templates/core/feedback.html`: analogous for `FeedbackForm`
- **Acceptance Criteria Addressed**: AC-1, AC-5, AC-6, AC-7
- **Test Requirements**:
  - `rule` TR-6.1: All 9 page templates extend `base.html` and render without syntax errors (Django `TemplateSyntaxError` absence confirmed by `python manage.py check --tag=templates`)
  - `rule` TR-6.2: Every internal `<a href>` and `<form action>` uses `{% url 'core:X' %}`; grep for bare `/registration/` etc. returns zero in templates dir (excluding comments)
  - `rubric` TR-6.3: 6-breakpoint modifier class usage breadth; scale 1-5; anchors 1=no modifiers, 3=md+lg only, 5=hero, cards, footer, typography all use responsive grid with -sm/-md/-lg/-xl/-xxl; threshold >= 4; evidence = template files
  - `rubric` TR-6.4: Glassmorphism class application on navbar/hero cards; scale 1-5; threshold >= 4; evidence = grep `.glass` and `.bg-gradient-deep` usage

## Task 7: Verification (syntax, check, makemigrations dry)
- **Status**: `pending`
- **Priority**: high
- **Depends On**: Task 1-6 completed
- **Description**:
  - Install deps, run `python manage.py check`, run `makemigrations --dry-run`, validate file list exists
- **Acceptance Criteria Addressed**: AC-1, AC-2, AC-3, AC-4, AC-5, AC-8, AC-9
- **Test Requirements**:
  - `rule` TR-7.1: `manage.py check` == exit 0
  - `rule` TR-7.2: `makemigrations --dry-run` succeeds (exit 0) and lists both models
  - `rule` TR-7.3: IDE diagnostics report no Python syntax errors in .py files
