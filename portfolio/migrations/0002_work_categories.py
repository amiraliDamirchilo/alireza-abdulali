from django.db import migrations, models
import django.db.models.deletion


DEFAULT_CATEGORIES = {
    "motion": ("Motion design", "طراحی موشن", 10),
    "edit": ("Film editing", "تدوین فیلم", 20),
    "brand": ("Brand film", "فیلم برند", 30),
    "3d": ("3D / CGI", "سه‌بعدی و CGI", 40),
}


def migrate_categories(apps, schema_editor):
    WorkCategory = apps.get_model("portfolio", "WorkCategory")
    Project = apps.get_model("portfolio", "Project")
    created = {}
    for slug, (name, name_fa, order) in DEFAULT_CATEGORIES.items():
        created[slug] = WorkCategory.objects.create(
            slug=slug, name=name, name_fa=name_fa, order=order
        )
    fallback = created["motion"]
    for project in Project.objects.all():
        project.category_fk = created.get(project.category, fallback)
        project.save(update_fields=["category_fk"])


class Migration(migrations.Migration):
    dependencies = [("portfolio", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="WorkCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, verbose_name="name")),
                ("name_fa", models.CharField(blank=True, max_length=80, verbose_name="Persian name")),
                ("slug", models.SlugField(unique=True)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "work category",
                "verbose_name_plural": "work categories",
                "ordering": ["order", "name"],
            },
        ),
        migrations.AddField(
            model_name="project",
            name="category_fk",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="projects", to="portfolio.workcategory"),
        ),
        migrations.RunPython(migrate_categories, migrations.RunPython.noop),
        migrations.RemoveField(model_name="project", name="category"),
        migrations.RenameField(model_name="project", old_name="category_fk", new_name="category"),
        migrations.AlterField(
            model_name="project",
            name="category",
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="projects", to="portfolio.workcategory"),
        ),
        migrations.AlterField(
            model_name="project",
            name="video_url",
            field=models.URLField(help_text="Paste a youtube.com, youtu.be, YouTube Shorts, or embed URL.", verbose_name="YouTube URL"),
        ),
        migrations.AlterModelOptions(name="project", options={"ordering": ["order", "-year", "title_en"], "verbose_name": "work", "verbose_name_plural": "works"}),
        migrations.AlterModelOptions(name="inquiry", options={"ordering": ["-created_at"], "verbose_name": "inbox message", "verbose_name_plural": "inbox messages"}),
    ]
