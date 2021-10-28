# Generated by Django 3.2.8 on 2021-10-28 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_request"),
    ]

    operations = [
        migrations.AlterField(
            model_name="submission",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="What’s your email?"),
        ),
        migrations.AlterField(
            model_name="submission",
            name="submitter",
            field=models.CharField(max_length=300, verbose_name="What’s your name?"),
        ),
    ]
