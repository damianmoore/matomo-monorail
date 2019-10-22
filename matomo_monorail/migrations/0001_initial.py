# Generated by Django 2.2.6 on 2019-10-22 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True)),
                ('type', models.CharField(choices=[('C', 'Client'), ('S', 'Server')], max_length=1)),
                ('method', models.CharField(max_length=6)),
                ('url', models.TextField(blank=True)),
                ('ip', models.CharField(blank=True, max_length=15)),
                ('user_agent', models.TextField(blank=True)),
                ('referer', models.TextField(blank=True)),
            ],
        ),
    ]
