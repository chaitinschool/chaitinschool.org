# Generated by Django 3.2.8 on 2021-10-28 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_auto_20211028_0116"),
    ]

    operations = [
        migrations.CreateModel(
            name="Request",
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
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("topic", models.TextField()),
            ],
        ),
    ]