# Generated by Django 4.0.4 on 2022-05-31 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0006_blogger_interests_blogger_occupation_blogger_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='profile_img',
            field=models.ImageField(default='data\x08lank-profile.png', upload_to=''),
        ),
    ]
