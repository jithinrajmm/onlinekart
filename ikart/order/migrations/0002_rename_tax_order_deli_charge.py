# Generated by Django 3.2.4 on 2021-07-04 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='tax',
            new_name='deli_charge',
        ),
    ]
