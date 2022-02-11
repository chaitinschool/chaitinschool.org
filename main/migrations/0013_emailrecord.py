# Generated by Django 4.0 on 2022-02-11 11:28

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_alter_workshop_transpired_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailRecord",
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
                ("subject", models.CharField(max_length=300)),
                ("body", models.TextField()),
                (
                    "sent_at",
                    models.DateTimeField(default=django.utils.timezone.now, null=True),
                ),
                ("email", models.EmailField(max_length=254)),
                (
                    "subscription",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="main.subscription",
                    ),
                ),
            ],
            options={
                "ordering": ["-sent_at"],
            },
        ),
    ]