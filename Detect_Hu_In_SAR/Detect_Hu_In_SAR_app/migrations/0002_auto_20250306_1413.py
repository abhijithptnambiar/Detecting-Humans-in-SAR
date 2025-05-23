# Generated by Django 2.0.9 on 2025-03-06 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Detect_Hu_In_SAR_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='detection',
            name='latitude',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detection',
            name='longitude',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rescue_team',
            name='latitude',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rescue_team',
            name='longitude',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
