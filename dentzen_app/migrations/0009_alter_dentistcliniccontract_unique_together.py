# Generated by Django 3.2.16 on 2022-12-14 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dentzen_app', '0008_alter_dentistcliniccontract_table'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dentistcliniccontract',
            unique_together={('clinic', 'dentist')},
        ),
    ]