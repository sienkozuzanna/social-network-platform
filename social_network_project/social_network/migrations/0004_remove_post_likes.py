# Generated by Django 4.2.17 on 2025-01-03 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("social_network", "0003_follow"),
    ]

    operations = [
        migrations.RemoveField(model_name="post", name="likes",),
    ]
