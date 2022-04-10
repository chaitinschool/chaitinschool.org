# Generated by Django 4.0 on 2022-04-02 01:26

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0019_alter_post_published_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
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
                ("email", models.EmailField(max_length=254)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("rsvp", models.BooleanField(default=True)),
                (
                    "workshop",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.workshop",
                    ),
                ),
            ],
            options={
                "ordering": ["-workshop"],
            },
        ),
    ]