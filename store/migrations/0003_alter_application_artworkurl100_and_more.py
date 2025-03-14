# Generated by Django 4.2.19 on 2025-03-02 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0002_application_artworkurl100_application_artworkurl512_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="artworkUrl100",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="application",
            name="artworkUrl512",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="application",
            name="artworkUrl60",
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="application",
            name="screenshotUrls",
            field=models.JSONField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="application",
            name="track_url",
            field=models.URLField(max_length=500),
        ),
    ]
