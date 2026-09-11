from django.shortcuts import redirect, render, reverse
from django.contrib import messages

from .forms import FeedbackForm, StudentRegistrationForm
from .utils import notify_feedback_submission, notify_registration_submission


STATIC_COURSES = [
    {
        'slug': 'magistr-hazirligi',
        'title': 'Magistr hazırlığı',
        'tag': 'Universitet',
        'duration': '6 ay',
        'summary': (
            'Magistratura qəbul imtahanlarına hələ hazırlıq: '
            'fənn üzrə mövzuların dərin öyrənilməsi, test həll üsulları və '
            'şəxsi mentor dəstəyi ilə yüksək nəticə əldə edin.'
        ),
        'topics': ['Diaqnostik test', 'Fənn əsasları', 'Praktik test çalışması', 'Son yoxlamalar'],
    },
    {
        'slug': 'dovlet-qullugu-hazirligi',
        'title': 'Dövlət qulluğu hazırlığı',
        'tag': 'Karyera',
        'duration': '4 ay',
        'summary': (
            'ASAN və Dövlət Qulluğu İmtahanlarına (DİM) tam hazırlıq proqramı. '
            'Məntiq, riyaziyyat, ümumi biliklər və Azərbaycan dili '
            'bölmələrində uzmanlaşmış müəllimlər tərəfindən tədris.'
        ),
        'topics': ['Məntiq və analitik təfəkkür', 'Riyaziyyat', 'Ümumi biliklər', 'Azərbaycan dili'],
    },
    {
        'slug': 'sat-prep',
        'title': 'SAT Preparation',
        'tag': 'University Prep',
        'duration': '12 həftə',
        'summary': (
            'Intensive preparation for the SAT covering evidence-based reading, '
            'writing, and math, with timed practice exams and personalized feedback.'
        ),
        'topics': ['Diagnostic assessment', 'Reading & Writing', 'Math deep dive', 'Full-length practice tests'],
    },
    {
        'slug': 'ielts',
        'title': 'IELTS Preparation',
        'tag': 'Language Proficiency',
        'duration': '10 həftə',
        'summary': (
            'Master all four IELTS sections — Listening, Reading, Writing, and Speaking — '
            'with mock exams and native-level coaching.'
        ),
        'topics': ['Listening strategies', 'Academic Reading', 'Writing Task 1 & 2', 'Speaking interview prep'],
    },
    {
        'slug': 'toefl',
        'title': 'TOEFL iBT Preparation',
        'tag': 'Language Proficiency',
        'duration': '10 həftə',
        'summary': (
            'Targeted TOEFL iBT prep with integrated skills training for reading, listening, '
            'speaking, and writing inside a computer-based environment.'
        ),
        'topics': ['Reading science passages', 'Listening note-taking', 'Speaking template mastery', 'Academic Writing'],
    },
    {
        'slug': 'math',
        'title': 'Riyaziyyat',
        'tag': 'Orta və Ali Məktəb',
        'duration': 'Tam il',
        'summary': (
            'Algebra, həndəsə, triqonometriya və təxmini hesablamaların '
            'konseptual öyrədilməsi — məntiqi düşüncə və problem həll bacarıqları.'
        ),
        'topics': ['Algebra & Funksiyalar', 'Həndəsə & Sübutlar', 'Triqonometriya', 'Təxmini Hesablamalar'],
    },
    {
        'slug': 'physics',
        'title': 'Fizika',
        'tag': 'Orta və Ali Məktəb',
        'duration': 'Tam il',
        'summary': (
            'Mexanikadan müasir fizikaya qədər eksperimentlə dəstəklənmiş '
            'fizika təlimi, anlayış və hesablama gücünün inkişafı.'
        ),
        'topics': ['Mexanika', 'Dalğalar & Optika', 'Elektrik & Maqnetizm', 'Müasir Fizika'],
    },
    {
        'slug': 'chemistry',
        'title': 'Kimya',
        'tag': 'Orta və Ali Məktəb',
        'duration': 'Tam il',
        'summary': (
            'Ümumi, üzvi və analitik kimyanın dərin konseptual öyrədilməsi '
            'və praktiki laboratoriya təcrübələri.'
        ),
        'topics': ['Atom Quruluşu', 'Stoikiometriya', 'Üzvi Kimya', 'Lab və Analiz'],
    },
    {
        'slug': 'biology',
        'title': 'Biologiya',
        'tag': 'Orta və Ali Məktəb',
        'duration': 'Tam il',
        'summary': (
            'Hüceyrə biologiyası, genetika, fiziologiya və ekologiyanın '
            'real case studilər və imtahan yönümlü problemlərlə öyrədilməsi.'
        ),
        'topics': ['Hüceyrə & Molekulyar', 'Genetika', 'Anatomiya & Fiziologiya', 'Ekologiya & Təkamül'],
    },
    {
        'slug': 'english',
        'title': 'İngilis dili',
        'tag': 'Dil Kursları',
        'duration': 'Hər bir dövr',
        'summary': (
            'Gündəlik, akademik və imtahan uğuru üçün danışıq səliqəsi, '
            'qrammatika, oxumaq və yazma bacarıqlarının inkişafı.'
        ),
        'topics': ['Danışıq ingiliscə', 'Qrammatika', 'Sürətli oxuma', 'Akademik yazı'],
    },
    {
        'slug': 'coding',
        'title': 'Proqramlaşdırma',
        'tag': 'STEM',
        'duration': '16 həftə',
        'summary': (
            'Layihə əsaslı Python və Veb əsasları. Tələbələr real proqramlar '
            'və portfoliolar qurur, hesablamalı düşüncəyi öyrənirlər.'
        ),
        'topics': ['Python əsasları', 'Alqoritmlər', 'Veb əsasları (HTML/CSS/JS)', 'Başlanğıc layihəsi'],
    },
]

STATIC_TEACHERS = [
    {'name': 'Aysel Məmmədova', 'role': 'İngilis dili və Sınaq Hazırlığı', 'initials': 'AM', 'bio': '15+ il sınaq hazırlığı təcrübəsi. Cambridge Sertifikatlı.'},
    {'name': 'Rəşid Hüseynov', 'role': 'Baş Riyaziyyat Müəllimi', 'initials': 'RH', 'bio': 'Olimpiada medalçısı, Riyaziyyat üzrə Magistr.'},
    {'name': 'Dr. Fəridə Abbasova', 'role': 'Fizika Şöbə Rəisi', 'initials': 'FA', 'bio': 'Elmlər namizədi. Eksperimentlər və robotikanı sevir.'},
    {'name': 'Vüqar Nəcəfov', 'role': 'Proqramlaşdırma və Robotika Məşqçisi', 'initials': 'VN', 'bio': 'Full-stack mühəndis, layihə əsasında tədris.'},
    {'name': 'Zərər Cəfərova', 'role': 'Kimya və Biologiya', 'initials': 'ZC', 'bio': 'Tibb təəssüratı arxa planı, canlı elmlərə həvəs.'},
    {'name': 'Eldar Quliyev', 'role': 'Azərbaycan dili və Ədəbiyyat', 'initials': 'EQ', 'bio': 'Yazıçı və ədəbiyyat şəxsi. Yazıçı tələbələri ilhamlandırır.'},
]

GALLERY_PROMPTS = [
    ('students-collaborating-modern-classroom-library-sunny-day', 'Tələbələr modern sinif otağında əməkdaşlıq edir'),
    ('physics-lab-experiment-high-school-students', 'Fizika laboratoriyasında eksperimentlər davam edir'),
    ('teacher-explaining-math-whiteboard-students-listening', 'Riyaziyyat müəllimi lövhədə izah edir'),
    ('robotics-club-students-arduino-soldering', 'Robotika klubu — tələbələr kodlaşdırır'),
    ('library-study-area-university-prep-students-reading', 'Sakit kitabxana tədris sahəsi'),
    ('graduation-ceremony-academy-students-smiling', 'Məktəbitmə mərasimi — xoşbəxt tələbələr'),
]


def _gallery_images():
    base = 'https://coresg-normal.trae.ai/api/ide/v1/text_to_image?image_size=landscape_4_3&prompt='
    from urllib.parse import quote
    return [
        {'url': base + quote(prompt), 'caption': caption}
        for prompt, caption in GALLERY_PROMPTS
    ]


def home(request):
    stats = [
        ('num', '2,500+', 'Tələbə'),
        ('num', '98%', 'İmtahan Uğur Dərəcəsi'),
        ('num', '45+', 'Peşəkar Müəllim'),
        ('num', '15', 'İllik Təcrübə'),
    ]
    testimonials = [
        ('Emin M.', 'Magistratura imtahanında yüksək bal topladım. Müəllimlər həqiqətən və kifayət qədər diqqət edir.', 5),
        ('Leyla K.', 'Dövlət qulluğu imtahanından 95+ bal aldım. Test çalışmaları çox reallaşırdı.', 5),
        ('Murad Y.', 'Robotika klubu ilin ən yaxşı hissəsi idi. Komandamız regional müsabiqədə qalib gəldi.', 4),
    ]
    return render(request, 'core/home.html', {'stats': stats, 'testimonials': testimonials})


def about(request):
    values = [
        ('🎯', 'Mükəmməllik', 'Ciddi kurikulum və hər tələbə üçün ölçülə bilən nəticələr.'),
        ('🤝', 'Səmədarlıq', 'Açıq irəliləyiş, dürüst rəy və valideyn tərəfdaşlığı.'),
        ('💡', 'İnnovasiya', 'Müasir alətlər, laboratoriyalar və müasir sinif üsulları.'),
        ('🧭', 'Rəhbərlik', 'Dərslərdən kənar mentorluq — karyeraların formalaşdırılması.'),
    ]
    return render(request, 'core/about.html', {'values': values})


def courses(request):
    return render(request, 'core/courses.html', {'courses': STATIC_COURSES})


def course_detail(request, slug):
    course = next((c for c in STATIC_COURSES if c['slug'] == slug), None)
    if course is None:
        from django.http import Http404
        raise Http404('Course not found')
    return render(request, 'core/course_detail.html', {'course': course})


def teachers(request):
    return render(request, 'core/teachers.html', {'teachers': STATIC_TEACHERS})


def gallery(request):
    return render(request, 'core/gallery.html', {'images': _gallery_images()})


def contact(request):
    return render(request, 'core/contact.html')


def registration(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            instance = form.save()
            notify_registration_submission(instance)
            messages.success(
                request,
                'Təşəkkür edirik! Qeydiyyatınız qəbul edildi. Komandamız qısa müddətdə sizinlə əlaqə saxlayacaq.',
            )
            return redirect(reverse('core:registration') + '#success')
        else:
            messages.error(
                request,
                'Formada bəzi səhvlər var. Zəhmət olmasa baxıb düzəldin.',
            )
    else:
        form = StudentRegistrationForm()
    return render(request, 'core/registration.html', {'form': form})


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            instance = form.save()
            notify_feedback_submission(instance)
            messages.success(
                request,
                'Rəyiniz üçün təşəkkür edirik! Paylaşdığınız üçün minnətdarıq.',
            )
            return redirect(reverse('core:feedback') + '#success')
        else:
            messages.error(
                request,
                'Rəy formasında bəzi səhvlər var. Zəhmət olmasa baxıb düzəldin.',
            )
    else:
        form = FeedbackForm()
    return render(request, 'core/feedback.html', {'form': form})
