# Generated by Django 2.2.26 on 2022-02-01 15:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('evangelisation', '0002_auto_20220123_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evangelisation',
            name='day',
            field=models.DateField(default=django.utils.timezone.now, verbose_name="Jour d'évangélisation"),
        ),
    ]