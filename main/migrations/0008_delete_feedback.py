# Generated by Django 4.1.1 on 2022-11-16 19:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0007_mentorship_is_available"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Feedback",
        ),
    ]
