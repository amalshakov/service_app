# Generated by Django 3.2.16 on 2024-03-07 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0007_auto_20240307_1939'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='subscription',
            index=models.Index(fields=['comment_a', 'comment_b'], name='services_su_comment_06a22e_idx'),
        ),
    ]