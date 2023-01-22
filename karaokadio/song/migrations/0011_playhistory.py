# Generated by Django 4.1.5 on 2023-01-21 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("song", "0010_remove_song_liked_by_song_like_count_like"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("played_at", models.DateTimeField(auto_now_add=True)),
                (
                    "played_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "song",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="song.song"
                    ),
                ),
            ],
            options={
                "ordering": ("-played_at",),
            },
        ),
    ]
