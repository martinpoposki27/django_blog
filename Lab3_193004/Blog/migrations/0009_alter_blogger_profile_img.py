# Generated by Django 4.0.4 on 2022-05-31 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0008_alter_blogger_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogger',
            name='profile_img',
            field=models.ImageField(default='data\\profile_imgs\x08lank-profile.png', upload_to='profile_imgs/'),
        ),
    ]
