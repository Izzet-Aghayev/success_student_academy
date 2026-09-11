import threading

import requests

from django.conf import settings
from django.core.mail import send_mail
from django.db import connections


def _close_db_after(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        finally:
            try:
                connections.close_all()
            except Exception:
                pass
    return wrapper


@_close_db_after
def send_telegram_message(token, chat_id, text):
    if not token or not chat_id:
        return False
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=12)
        return resp.status_code == 200 and resp.json().get('ok') is True
    except Exception:
        return False


@_close_db_after
def send_email_notification(subject, plain_message, html_message, from_email, recipient_list):
    if not recipient_list:
        return False
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=True,
        )
        return True
    except Exception:
        return False


def _registration_telegram_text(instance):
    return (
        '🎓 <b>Yeni Tələbə Qeydiyyatı</b>\n\n'
        f'<b>Ad:</b> {instance.ad}\n'
        f'<b>Soyad:</b> {instance.soyad}\n'
        f'<b>Xidmət:</b> {instance.get_xidmet_display()}\n'
        f'<b>Əlaqə nömrəsi:</b> {instance.elaqe_nomresi}\n'
        f'<b>Mesaj:</b> {instance.mesaj or "-"}\n'
        f'<b>Tarix:</b> {instance.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
    )


def _feedback_telegram_text(instance):
    return (
        '📝 <b>Yeni Rəy</b>\n\n'
        f'<b>Rəy mətni:</b>\n{instance.rey_metni}\n\n'
        f'<b>Tarix:</b> {instance.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
    )


def _registration_email(instance):
    subject = f'Yeni Qeydiyyat — {instance.ad} {instance.soyad}'
    plain_lines = [
        f'Ad: {instance.ad}',
        f'Soyad: {instance.soyad}',
        f'Xidmət: {instance.get_xidmet_display()}',
        f'Əlaqə nömrəsi: {instance.elaqe_nomresi}',
        f'Mesaj: {instance.mesaj or "-"}',
        f'Tarix: {instance.created_at.strftime("%Y-%m-%d %H:%M:%S")}',
    ]
    plain_message = '\n'.join(plain_lines)
    rows_html = ''.join(
        f'<tr><td style="padding:6px 10px;font-weight:600;color:#0f172a;">{label}</td>'
        f'<td style="padding:6px 10px;color:#0f172a;">{value}</td></tr>'
        for label, value in [
            ('Ad', instance.ad),
            ('Soyad', instance.soyad),
            ('Xidmət', instance.get_xidmet_display()),
            ('Əlaqə nömrəsi', instance.elaqe_nomresi),
            ('Mesaj', instance.mesaj or '-'),
            ('Tarix', instance.created_at.strftime('%Y-%m-%d %H:%M:%S')),
        ]
    )
    html_message = (
        '<div style="font-family:Arial,sans-serif;max-width:680px;margin:auto;'
        'padding:24px;background:#f8fafc;border-radius:16px;">'
        '<h2 style="color:#1e3a8a;margin:0 0 16px;">🎓 Yeni Tələbə Qeydiyyatı</h2>'
        f'<table style="width:100%;background:#fff;border-radius:12px;border-collapse:collapse;'
        f'box-shadow:0 6px 24px rgba(15,23,42,.08);">{rows_html}</table></div>'
    )
    return subject, plain_message, html_message


def _feedback_email(instance):
    subject = 'Yeni Rəy — SUCCESS STUDENT ACADEMY'
    plain_lines = [
        'Rəy mətni:',
        instance.rey_metni,
        '',
        f'Tarix: {instance.created_at.strftime("%Y-%m-%d %H:%M:%S")}',
    ]
    plain_message = '\n'.join(plain_lines)
    html_message = (
        '<div style="font-family:Arial,sans-serif;max-width:680px;margin:auto;'
        'padding:24px;background:#f8fafc;border-radius:16px;">'
        '<h2 style="color:#1e3a8a;margin:0 0 16px;">📝 Yeni Rəy</h2>'
        '<div style="background:#fff;border-radius:12px;padding:22px;'
        'box-shadow:0 6px 24px rgba(15,23,42,.08);">'
        f'<p style="margin:16px 0 4px;"><b>Rəy mətni:</b></p>'
        f'<pre style="white-space:pre-wrap;margin:0;background:#f1f5f9;padding:12px;border-radius:10px;'
        f'font-family:Arial,sans-serif;">{instance.rey_metni}</pre>'
        f'<p style="margin:16px 0 0;color:#64748b;font-size:0.9rem;">'
        f'Tarix: {instance.created_at.strftime("%Y-%m-%d %H:%M:%S")}</p>'
        '</div></div>'
    )
    return subject, plain_message, html_message


def notify_registration_submission(instance):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '')
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
    recipient = getattr(settings, 'CONTACT_EMAIL_RECIPIENT', from_email)
    recipients = [r.strip() for r in recipient.split(',') if r.strip()]

    tg_text = _registration_telegram_text(instance)
    subj, plain_text, html_text = _registration_email(instance)

    t1 = threading.Thread(
        target=send_telegram_message,
        args=(token, chat_id, tg_text),
        daemon=True,
    )
    t2 = threading.Thread(
        target=send_email_notification,
        args=(subj, plain_text, html_text, from_email, recipients),
        daemon=True,
    )
    t1.start()
    t2.start()


def notify_feedback_submission(instance):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', '')
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', '')
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com')
    recipient = getattr(settings, 'CONTACT_EMAIL_RECIPIENT', from_email)
    recipients = [r.strip() for r in recipient.split(',') if r.strip()]

    tg_text = _feedback_telegram_text(instance)
    subj, plain_text, html_text = _feedback_email(instance)

    t1 = threading.Thread(
        target=send_telegram_message,
        args=(token, chat_id, tg_text),
        daemon=True,
    )
    t2 = threading.Thread(
        target=send_email_notification,
        args=(subj, plain_text, html_text, from_email, recipients),
        daemon=True,
    )
    t1.start()
    t2.start()
