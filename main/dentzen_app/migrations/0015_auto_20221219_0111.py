# Generated by Django 3.2.16 on 2022-12-19 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dentzen_app', '0014_alter_dentistcliniccontract_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='drug',
            name='age_restriction',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='drug',
            name='volume',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='instrument',
            name='is_reusable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='instrument',
            name='weight',
            field=models.FloatField(default=0.0),
        ),
    ]
