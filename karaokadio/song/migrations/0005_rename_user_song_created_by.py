# Generated by Django 4.1.5 on 2023-01-15 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("song", "0004_song_title_alter_song_file"),
    ]

    operations = [
        migrations.RenameField(
            model_name="song",
            old_name="user",
            new_name="created_by",
        ),
    ]
