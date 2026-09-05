from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Inquiry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("company", models.CharField(blank=True, max_length=120)),
                ("service", models.CharField(choices=[("motion", "Motion design"), ("edit", "Film editing"), ("brand", "Brand film"), ("cgi", "3D / CGI"), ("other", "Something else")], max_length=20)),
                ("budget", models.CharField(blank=True, max_length=50)),
                ("message", models.TextField()),
                ("is_read", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title_en", models.CharField(max_length=120)),
                ("title_fa", models.CharField(blank=True, max_length=120)),
                ("slug", models.SlugField(unique=True)),
                ("client", models.CharField(blank=True, max_length=100)),
                ("year", models.PositiveSmallIntegerField(default=2026)),
                ("category", models.CharField(choices=[("motion", "Motion design"), ("edit", "Film editing"), ("brand", "Brand film"), ("3d", "3D / CGI")], default="motion", max_length=20)),
                ("summary_en", models.TextField(blank=True)),
                ("summary_fa", models.TextField(blank=True)),
                ("cover", models.ImageField(blank=True, upload_to="projects/")),
                ("video_url", models.URLField(blank=True)),
                ("accent", models.CharField(default="#a600ff", help_text="Hex color, e.g. #a600ff", max_length=7, validators=[django.core.validators.RegexValidator("^#[0-9a-fA-F]{6}$", "Use a six-digit hex color.")])),
                ("featured", models.BooleanField(default=True)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["order", "-year", "title_en"]},
        ),
    ]
