# Generated by Django 3.2.4 on 2021-07-18 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_refferal_user_recomended_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='refferal_coupen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_coupon', models.CharField(max_length=20)),
                ('ref_percentage', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
