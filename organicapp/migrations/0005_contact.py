# Generated by Django 4.2.1 on 2023-06-09 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organicapp', '0004_orderhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('email', models.CharField(max_length=400)),
                ('mobile', models.IntegerField()),
                ('message', models.CharField(max_length=1000)),
            ],
        ),
    ]
