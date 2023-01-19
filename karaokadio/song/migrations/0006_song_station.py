# Generated by Django 4.1.5 on 2023-01-19 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("station", "0002_station_created_by"),
        ("song", "0005_rename_user_song_created_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="song",
            name="station",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="station.station",
            ),
        ),
    ]
