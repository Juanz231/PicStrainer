# Generated by Django 4.2.5 on 2023-10-18 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Docs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='type',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='doc',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
