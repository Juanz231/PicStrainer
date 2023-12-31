# Generated by Django 4.2.5 on 2023-10-18 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pic', '0007_image_age_image_emotion_image_gender_image_race'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='emotion',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='gender',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='race',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
