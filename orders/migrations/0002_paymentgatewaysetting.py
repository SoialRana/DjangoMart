# Generated by Django 4.2.3 on 2023-09-01 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentGateWaySetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.CharField(blank=True, max_length=500, null=True)),
                ('store_pass', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]