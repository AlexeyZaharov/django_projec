# Generated by Django 2.1.7 on 2019-04-15 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asker', '0005_auto_20190415_1714'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answers',
        ),
        migrations.AddField(
            model_name='question',
            name='answers',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='asker.Answers'),
        ),
    ]