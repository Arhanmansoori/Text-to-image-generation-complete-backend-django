# Generated by Django 5.1.7 on 2025-03-15 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prompt', models.TextField()),
                ('image', models.ImageField(upload_to='generated_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
