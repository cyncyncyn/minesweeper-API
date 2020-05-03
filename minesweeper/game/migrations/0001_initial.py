# Generated by Django 3.0.3 on 2020-05-03 16:52

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('width', models.PositiveIntegerField(default=8)),
                ('height', models.PositiveIntegerField(default=8)),
                ('amount_of_mines', models.PositiveIntegerField(default=10)),
                ('status', models.CharField(choices=[('PLY', 'Playing'), ('WON', 'Won'), ('LST', 'Lost')], default='PLY', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.PositiveIntegerField()),
                ('col', models.PositiveIntegerField()),
                ('flagged', models.BooleanField(default=False)),
                ('is_mine', models.BooleanField(default=False)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Board')),
            ],
        ),
    ]