from django.contrib import admin
from django import forms
from .models import Inquiry, Project, Service, SiteText, WorkCategory


admin.site.site_header = "."
admin.site.site_title = "."
admin.site.index_title = "."


class SiteTextAdminForm(forms.ModelForm):
    class Meta:
        model = SiteText
        fields = "__all__"
        widgets = {
            "text_en": forms.Textarea(attrs={"rows": 3}),
            "text_fa": forms.Textarea(attrs={"rows": 3, "dir": "rtl"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        limit = self.instance.character_limit if self.instance and self.instance.pk else 180
        for name in ("text_en", "text_fa"):
            self.fields[name].widget.attrs["maxlength"] = limit
            self.fields[name].help_text = f"Maximum {limit} characters — plain text only."


@admin.register(SiteText)
class SiteTextAdmin(admin.ModelAdmin):
    form = SiteTextAdminForm
    list_display = ("label", "section", "english_preview", "persian_preview", "character_limit")
    list_filter = ("section",)
    search_fields = ("label", "text_en", "text_fa")
    readonly_fields = ("section", "key", "label", "character_limit")
    ordering = ("id",)
    list_per_page = 30
    fieldsets = (
        ("Location & safety", {"fields": ("section", "label", "key", "character_limit")}),
        ("Editable copy", {"fields": ("text_en", "text_fa"), "description": "Only plain text is accepted. Character limits keep the public layout stable."}),
    )

    @admin.display(description="English")
    def english_preview(self, obj):
        return obj.text_en[:70]

    @admin.display(description="فارسی")
    def persian_preview(self, obj):
        return obj.text_fa[:70]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "service_name", "title_en", "title_fa", "description_en",
        "description_fa", "deliverables_en", "deliverables_fa", "order", "is_active",
    )
    list_display_links = ("service_name",)
    list_editable = (
        "title_en", "title_fa", "description_en", "description_fa",
        "deliverables_en", "deliverables_fa", "order", "is_active",
    )
    search_fields = ("title_en", "title_fa", "description_en", "description_fa")
    prepopulated_fields = {"slug": ("title_en",)}
    save_on_top = True
    fieldsets = (
        ("Service", {"fields": ("title_en", "title_fa", "slug")}),
        ("Description", {"fields": ("description_en", "description_fa")}),
        ("Deliverables", {"fields": ("deliverables_en", "deliverables_fa")}),
        ("Display", {"fields": ("order", "is_active")}),
    )

    @admin.display(description="Card")
    def service_name(self, obj):
        return f"#{obj.order} — {obj.title_en}"


@admin.register(WorkCategory)
class WorkCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "name_fa", "project_count", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "name_fa")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Works")
    def project_count(self, obj):
        return obj.projects.count()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title_en", "client", "category", "year", "featured", "order")
    list_editable = ("featured", "order")
    list_filter = ("category", "featured", "year")
    search_fields = ("title_en", "title_fa", "client", "category__name")
    autocomplete_fields = ("category",)
    prepopulated_fields = {"slug": ("title_en",)}
    save_on_top = True
    fieldsets = (
        ("Work details", {"fields": ("title_en", "title_fa", "slug", "category", "client", "year")}),
        ("Title & description", {"fields": ("summary_en", "summary_fa")}),
        ("YouTube & display", {"fields": ("video_url", "cover", "accent", "featured", "order"), "description": "Paste the YouTube link. The site embeds the video automatically."}),
    )


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "service", "company", "is_read", "created_at")
    list_editable = ("is_read",)
    list_filter = ("is_read", "service", "created_at")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("name", "email", "company", "service", "budget", "message", "created_at")
    date_hierarchy = "created_at"
    list_per_page = 30
    actions = ("mark_as_read", "mark_as_unread")

    @admin.action(description="Mark selected messages as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

    def has_add_permission(self, request):
        return False
