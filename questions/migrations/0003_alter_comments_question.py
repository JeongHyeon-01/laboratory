# Generated by Django 4.0.4 on 2022-05-19 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_questions_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='questions.questions'),
        ),
    ]
