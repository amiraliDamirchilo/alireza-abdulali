from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from urllib.parse import parse_qs, urlparse
import re


class WorkCategory(models.Model):
    name = models.CharField("name", max_length=80)
    name_fa = models.CharField("Persian name", max_length=80, blank=True)
    slug = models.SlugField(unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "work category"
        verbose_name_plural = "work categories"

    def __str__(self):
        return self.name


class SiteText(models.Model):
    class Section(models.TextChoices):
        NAVIGATION = "navigation", "Navigation"
        HERO = "hero", "Hero"
        WORK = "work", "Work"
        ABOUT = "about", "About"
        SERVICES = "services", "Services"
        CONTACT = "contact", "Contact"

    section = models.CharField(max_length=20, choices=Section.choices)
    key = models.SlugField(max_length=60, unique=True)
    label = models.CharField(max_length=80)
    text_en = models.TextField("English text")
    text_fa = models.TextField("Persian text")
    character_limit = models.PositiveSmallIntegerField(default=180)

    class Meta:
        ordering = ["section", "id"]
        verbose_name = "site text"
        verbose_name_plural = "site texts"

    def __str__(self):
        return f"{self.get_section_display()} — {self.label}"

    def clean(self):
        super().clean()
        errors = {}
        if len(self.text_en) > self.character_limit:
            errors["text_en"] = f"Keep this text under {self.character_limit} characters to protect the layout."
        if len(self.text_fa) > self.character_limit:
            errors["text_fa"] = f"متن برای حفظ چیدمان باید حداکثر {self.character_limit} کاراکتر باشد."
        if errors:
            raise ValidationError(errors)


class Service(models.Model):
    title_en = models.CharField("English title", max_length=45)
    title_fa = models.CharField("Persian title", max_length=45)
    slug = models.SlugField(unique=True)
    description_en = models.CharField("English description", max_length=220)
    description_fa = models.CharField("Persian description", max_length=220)
    deliverables_en = models.CharField("English deliverables", max_length=80, blank=True)
    deliverables_fa = models.CharField("Persian deliverables", max_length=80, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "service card"
        verbose_name_plural = "service cards"

    def __str__(self):
        return self.title_en


class Project(models.Model):
    title_en = models.CharField(max_length=120)
    title_fa = models.CharField(max_length=120, blank=True)
    slug = models.SlugField(unique=True)
    client = models.CharField(max_length=100, blank=True)
    year = models.PositiveSmallIntegerField(default=2026)
    category = models.ForeignKey(WorkCategory, on_delete=models.PROTECT, related_name="projects")
    summary_en = models.TextField(blank=True)
    summary_fa = models.TextField(blank=True)
    cover = models.ImageField(upload_to="projects/", blank=True)
    video_url = models.URLField(
        "YouTube URL",
        help_text="Paste a youtube.com, youtu.be, YouTube Shorts, or embed URL.",
    )
    accent = models.CharField(
        max_length=7,
        default="#a600ff",
        validators=[RegexValidator(r"^#[0-9a-fA-F]{6}$", "Use a six-digit hex color.")],
        help_text="Hex color, e.g. #a600ff",
    )
    featured = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-year", "title_en"]
        verbose_name = "work"
        verbose_name_plural = "works"

    def __str__(self):
        return self.title_en

    @staticmethod
    def youtube_video_id(url):
        """Return the video id for common YouTube URL formats."""
        if not url:
            return ""
        parsed = urlparse(url.strip())
        host = parsed.netloc.lower().removeprefix("www.").removeprefix("m.")
        if host == "youtu.be":
            return parsed.path.strip("/").split("/")[0]
        if host in {"youtube.com", "youtube-nocookie.com"}:
            if parsed.path == "/watch":
                return parse_qs(parsed.query).get("v", [""])[0]
            parts = [part for part in parsed.path.split("/") if part]
            if len(parts) >= 2 and parts[0] in {"embed", "shorts", "live"}:
                return parts[1]
        return ""

    @property
    def youtube_embed_url(self):
        video_id = self.youtube_video_id(self.video_url)
        return f"https://www.youtube-nocookie.com/embed/{video_id}" if video_id else ""

    def clean(self):
        super().clean()
        video_id = self.youtube_video_id(self.video_url)
        if not re.fullmatch(r"[A-Za-z0-9_-]{6,20}", video_id):
            raise ValidationError({"video_url": "Enter a valid YouTube video URL."})


class Inquiry(models.Model):
    class Service(models.TextChoices):
        MOTION = "motion", "Motion design"
        EDIT = "edit", "Film editing"
        BRAND = "brand", "Brand film"
        CGI = "cgi", "3D / CGI"
        OTHER = "other", "Something else"

    name = models.CharField(max_length=100)
    email = models.EmailField()
    company = models.CharField(max_length=120, blank=True)
    service = models.CharField(max_length=20, choices=Service.choices)
    budget = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "inbox message"
        verbose_name_plural = "inbox messages"

    def __str__(self):
        return f"{self.name} — {self.get_service_display()}"
