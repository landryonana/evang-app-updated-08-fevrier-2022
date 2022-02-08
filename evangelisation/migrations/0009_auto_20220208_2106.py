# Generated by Django 2.2.26 on 2022-02-08 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('evangelisation', '0008_auto_20220208_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suivi',
            name='person',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suivis', to='evangelisation.Person', verbose_name='Personne'),
        ),
    ]
