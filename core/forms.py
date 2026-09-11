import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Feedback, StudentRegistration, XIDMET_CHOICES


PHONE_RE = re.compile(r'^[+\d][\d\s\-\(\)\.]{7,30}$')


class StudentRegistrationForm(forms.ModelForm):
    xidmet = forms.ChoiceField(
        choices=XIDMET_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    mesaj = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': 500}),
    )

    class Meta:
        model = StudentRegistration
        fields = ('ad', 'soyad', 'xidmet', 'elaqe_nomresi', 'mesaj')
        widgets = {
            'ad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız'}),
            'soyad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyadınız'}),
            'elaqe_nomresi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+994 50 123 45 67'}),
        }
        labels = {
            'ad': 'Ad',
            'soyad': 'Soyad',
            'xidmet': 'Xidmət',
            'elaqe_nomresi': 'Əlaqə nömrəsi',
            'mesaj': 'Mesaj (istəyə bağlı)',
        }

    def clean_elaqe_nomresi(self):
        nomre = self.cleaned_data.get('elaqe_nomresi', '')
        if not PHONE_RE.match(nomre):
            raise ValidationError('Zəhmət olmasa düzgün əlaqə nömrəsi daxil edin.')
        return nomre


class FeedbackForm(forms.ModelForm):
    rey_metni = forms.CharField(
        max_length=1500,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'maxlength': 1500}),
    )

    class Meta:
        model = Feedback
        fields = ('rey_metni',)
        labels = {
            'rey_metni': 'Rəy mətni',
        }
