# Generated by Django 2.0.9 on 2025-01-02 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Detect_Hu_In_SAR_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='work_allocation',
            name='date',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
