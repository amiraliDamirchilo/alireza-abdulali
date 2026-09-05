from django.db import migrations, models


def seed_site_texts(apps, schema_editor):
    SiteText = apps.get_model("portfolio", "SiteText")
    from portfolio.site_copy import DEFAULT_SITE_TEXTS

    SiteText.objects.bulk_create([
        SiteText(
            section=section,
            key=key,
            label=label,
            text_en=text_en,
            text_fa=text_fa,
            character_limit=limit,
        )
        for section, key, label, text_en, text_fa, limit in DEFAULT_SITE_TEXTS
    ])


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0002_work_categories")]

    operations = [
        migrations.CreateModel(
            name="SiteText",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("section", models.CharField(choices=[("navigation", "Navigation"), ("hero", "Hero"), ("work", "Work"), ("about", "About"), ("services", "Services"), ("contact", "Contact")], max_length=20)),
                ("key", models.SlugField(max_length=60, unique=True)),
                ("label", models.CharField(max_length=80)),
                ("text_en", models.TextField(verbose_name="English text")),
                ("text_fa", models.TextField(verbose_name="Persian text")),
                ("character_limit", models.PositiveSmallIntegerField(default=180)),
            ],
            options={"ordering": ["section", "id"], "verbose_name": "site text", "verbose_name_plural": "site texts"},
        ),
        migrations.RunPython(seed_site_texts, migrations.RunPython.noop),
    ]
