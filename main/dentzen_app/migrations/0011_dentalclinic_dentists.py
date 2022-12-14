# Generated by Django 3.2.16 on 2022-12-14 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dentzen_app', '0010_remove_dentalclinic_dentists'),
    ]

    operations = [
        migrations.AddField(
            model_name='dentalclinic',
            name='dentists',
            field=models.ManyToManyField(through='dentzen_app.DentistClinicContract', to='dentzen_app.Dentist'),
        ),
    ]
