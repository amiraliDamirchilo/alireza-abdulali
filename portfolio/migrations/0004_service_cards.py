from django.db import migrations, models


SERVICES = [
    ("motionDesign", "motionDescription", "motionDeliverables", "Motion design", "طراحی موشن", "motion-design", "Motion identities, title sequences and campaign systems built to hold attention.", "هویت متحرک، تیتراژ و سیستم‌های کمپین برای جلب و حفظ توجه.", "IDENTITY · TITLES · CAMPAIGNS", "هویت · تیتراژ · کمپین", 10),
    ("filmEditing", "editDescription", "editDeliverables", "Film editing", "تدوین فیلم", "film-editing", "Story, pacing and sound brought together in one deliberate editorial rhythm.", "ترکیب داستان، ریتم و صدا در یک تدوین دقیق و هدفمند.", "STORY · RHYTHM · SOUND", "داستان · ریتم · صدا", 20),
    ("artDirection", "artDescription", "artDeliverables", "Art direction", "هدایت هنری", "art-direction", "A distinct visual language that stays coherent from concept to delivery.", "یک زبان بصری متمایز و منسجم، از ایده تا خروجی نهایی.", "CONCEPT · STYLE · SYSTEM", "ایده · استایل · سیستم", 30),
    ("cgi", "cgiDescription", "cgiDeliverables", "CGI / 3D", "سه‌بعدی و CGI", "cgi-3d", "Purposeful digital worlds and product visuals with convincing material detail.", "دنیاها و تصاویر محصول با جزئیات متریال باورپذیر و هدفمند.", "WORLDS · PRODUCT · SIMULATION", "دنیا · محصول · شبیه‌سازی", 40),
]


def seed_services(apps, schema_editor):
    Service = apps.get_model("portfolio", "Service")
    SiteText = apps.get_model("portfolio", "SiteText")
    rows = []
    keys_to_remove = []
    for title_key, description_key, deliverables_key, title_en, title_fa, slug, description_en, description_fa, deliverables_en, deliverables_fa, order in SERVICES:
        values = {}
        for field, key, fallback_en, fallback_fa in (
            ("title", title_key, title_en, title_fa),
            ("description", description_key, description_en, description_fa),
            ("deliverables", deliverables_key, deliverables_en, deliverables_fa),
        ):
            old = SiteText.objects.filter(key=key).first()
            values[f"{field}_en"] = old.text_en if old else fallback_en
            values[f"{field}_fa"] = old.text_fa if old else fallback_fa
            keys_to_remove.append(key)
        rows.append(Service(slug=slug, order=order, **values))
    Service.objects.bulk_create(rows)
    SiteText.objects.filter(key__in=keys_to_remove).delete()


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0003_site_texts")]

    operations = [
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title_en", models.CharField(max_length=45, verbose_name="English title")),
                ("title_fa", models.CharField(max_length=45, verbose_name="Persian title")),
                ("slug", models.SlugField(unique=True)),
                ("description_en", models.CharField(max_length=220, verbose_name="English description")),
                ("description_fa", models.CharField(max_length=220, verbose_name="Persian description")),
                ("deliverables_en", models.CharField(blank=True, max_length=80, verbose_name="English deliverables")),
                ("deliverables_fa", models.CharField(blank=True, max_length=80, verbose_name="Persian deliverables")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["order", "id"], "verbose_name": "service card", "verbose_name_plural": "service cards"},
        ),
        migrations.RunPython(seed_services, migrations.RunPython.noop),
    ]
