# Generated by Django 4.2.4 on 2023-08-15 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='imagenes')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
