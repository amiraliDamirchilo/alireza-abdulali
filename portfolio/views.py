from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.views.decorators.http import require_POST

from .forms import InquiryForm
from .models import Project, Service, SiteText, WorkCategory
from .site_copy import DEFAULT_SITE_TEXT_MAP


DEMO_PROJECTS = [
    {
        "title_en": "NEON PULSE", "title_fa": "ضربان نئون", "category": "motion",
        "category_en": "Motion design", "category_fa": "طراحی موشن", "year": 2026,
        "client": "Vanta", "accent": "#a600ff", "index": "01",
        "summary_en": "A kinetic identity built around rhythm, contrast and instant recognition.",
        "summary_fa": "هویتی پویا بر پایهٔ ریتم، کنتراست و تشخیص سریع.",
    },
    {
        "title_en": "ZERO GRAVITY", "title_fa": "جاذبه صفر", "category": "3d",
        "category_en": "3D / CGI", "category_fa": "سه‌بعدی و CGI", "year": 2026,
        "client": "Orbit", "accent": "#6e44ff", "index": "02",
        "summary_en": "A weightless product world shaped with precise CGI and tactile light.",
        "summary_fa": "دنیایی بی‌وزن با CGI دقیق و نورپردازی ملموس.",
    },
    {
        "title_en": "AFTER IMAGE", "title_fa": "پس‌تصویر", "category": "edit",
        "category_en": "Film editing", "category_fa": "تدوین فیلم", "year": 2025,
        "client": "Noir", "accent": "#e05cff", "index": "03",
        "summary_en": "An editorial film where pace, sound and silence carry the story.",
        "summary_fa": "فیلمی تدوین‌محور که ریتم، صدا و سکوت داستانش را پیش می‌برند.",
    },
    {
        "title_en": "RAW SIGNAL", "title_fa": "سیگنال خام", "category": "brand",
        "category_en": "Brand film", "category_fa": "فیلم برند", "year": 2025,
        "client": "FWD", "accent": "#7b00ff", "index": "04",
        "summary_en": "A bold brand film turning raw energy into one coherent visual system.",
        "summary_fa": "فیلمی جسور که انرژی خام را به یک سیستم بصری منسجم تبدیل می‌کند.",
    },
]

CATEGORY_LABELS_FA = {
    "motion": "طراحی موشن",
    "edit": "تدوین فیلم",
    "brand": "فیلم برند",
    "3d": "سه‌بعدی و CGI",
}


def _project_list(limit=None):
    queryset = Project.objects.filter(featured=True, category__is_active=True).exclude(video_url="").select_related("category")
    projects = list(queryset[:limit] if limit else queryset)
    for index, project in enumerate(projects, start=1):
        project.index = f"{index:02d}"
        project.category_en = project.category.name
        project.category_fa = project.category.name_fa or project.category.name
    return projects


def _page_context(request, page_name, **extra):
    site_copy = {key: values.copy() for key, values in DEFAULT_SITE_TEXT_MAP.items()}
    for item in SiteText.objects.all().only("key", "text_en", "text_fa"):
        if item.key in site_copy:
            site_copy[item.key] = {"en": item.text_en, "fa": item.text_fa}
    return {
        "page_name": page_name,
        "og_image": request.build_absolute_uri(static("images/portrait.png")),
        "site_copy": site_copy,
        **extra,
    }


def home(request):
    projects = _project_list()
    return render(
        request,
        "portfolio/home.html",
        _page_context(
            request,
            "home",
            projects=projects,
            featured_projects=projects[:3],
            categories=WorkCategory.objects.filter(is_active=True),
            services=Service.objects.filter(is_active=True),
            form=InquiryForm(),
        ),
    )


def work(request):
    return redirect("/?section=work#work")


def about(request):
    return redirect("/?section=about#about")


def services(request):
    return redirect("/?section=services#services")


def contact(request):
    return redirect("/?section=contact#contact")


@require_POST
def submit_inquiry(request):
    form = InquiryForm(request.POST)
    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    if form.is_valid():
        form.save()
        if is_ajax:
            return JsonResponse({"ok": True, "message": "Your brief is in. I'll reply shortly."})
        messages.success(request, "Your brief is in. I'll reply shortly.")
        return redirect("/?sent=1#contact")
    if is_ajax:
        return JsonResponse({"ok": False, "errors": form.errors.get_json_data()}, status=400)
    projects = _project_list()
    return render(request, "portfolio/home.html", _page_context(
        request, "home", projects=projects, featured_projects=projects[:3],
        categories=WorkCategory.objects.filter(is_active=True), form=form,
        services=Service.objects.filter(is_active=True),
    ), status=400)
