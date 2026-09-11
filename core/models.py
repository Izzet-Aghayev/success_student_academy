from django.db import models


XIDMET_CHOICES = [
    ('magistr', 'Magistr hazırlığı'),
    ('dovlet_qullugu', 'Dövlət qulluğu hazırlığı'),
    ('sat_prep', 'SAT Preparation'),
    ('ielts', 'IELTS Preparation'),
    ('toefl', 'TOEFL Preparation'),
    ('math', 'Riyaziyyat'),
    ('physics', 'Fizika'),
    ('chemistry', 'Kimya'),
    ('biology', 'Biologiya'),
    ('english', 'İngilis dili'),
    ('coding', 'Proqramlaşdırma'),
]


class StudentRegistration(models.Model):
    ad = models.CharField(max_length=100)
    soyad = models.CharField(max_length=100)
    xidmet = models.CharField(max_length=50, choices=XIDMET_CHOICES)
    elaqe_nomresi = models.CharField(max_length=30)
    mesaj = models.TextField(max_length=500, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Student Registration'
        verbose_name_plural = 'Student Registrations'

    def __str__(self):
        return f'{self.ad} {self.soyad} — {self.get_xidmet_display()}'


class Feedback(models.Model):
    rey_metni = models.TextField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedback Entries'

    def __str__(self):
        snippet = self.rey_metni[:60]
        return f'{snippet}{"…" if len(self.rey_metni) > 60 else ""}'
