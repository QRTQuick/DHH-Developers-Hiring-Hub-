# Generated manually to remove password field from PlatformUser
# Password is now handled by Django's built-in User model

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DeveloperHieringHub', '0002_emailotp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platformuser',
            name='password',
        ),
    ]
