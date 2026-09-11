from django.contrib import admin

from .models import Feedback, StudentRegistration


@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        'ad',
        'soyad',
        'xidmet',
        'elaqe_nomresi',
        'created_at',
    )
    list_filter = (
        'xidmet',
        'created_at',
    )
    search_fields = (
        'ad',
        'soyad',
        'elaqe_nomresi',
        'mesaj',
    )
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'rey_metni_short',
        'created_at',
    )
    list_filter = ('created_at',)
    search_fields = ('rey_metni',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def rey_metni_short(self, obj):
        text = obj.rey_metni
        return text[:80] + ('…' if len(text) > 80 else '')
    rey_metni_short.short_description = 'Rəy'
