# Generated by Django 3.2.16 on 2023-04-17 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('katz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='catID',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
