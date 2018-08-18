# Generated by Django 2.0.4 on 2018-08-15 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('chapter_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Torrent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_subtitle', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('finished', 'finished'), ('paused', 'paused'), ('cancelled', 'cancelled'), ('in_progress', 'in_progress')], max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='video',
            name='type',
            field=models.CharField(choices=[('TVSHOW', 'TV Show'), ('MOVIE', 'Movie')], max_length=6),
        ),
        migrations.AddField(
            model_name='season',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='video.Video'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='video.Season'),
        ),
        migrations.AddField(
            model_name='chapter',
            name='torrent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='show', to='video.Torrent'),
        ),
        migrations.AddField(
            model_name='video',
            name='torrent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='video.Torrent'),
        ),
    ]
