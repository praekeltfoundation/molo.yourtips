# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-23 06:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import molo.core.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0062_increase_char_length_reaction_success'),
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('yourtips', '0004_auto_20170620_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='YourTipsArticleIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', molo.core.models.PreventDeleteMixin),
        ),
        migrations.CreateModel(
            name='YourTipsEntryPage',
            fields=[
                ('articlepage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.ArticlePage')),
            ],
            options={
                'abstract': False,
            },
            bases=('core.articlepage',),
        ),
        migrations.RenameField(
            model_name='yourtipsentry',
            old_name='terms_or_conditions_approved',
            new_name='allow_share_on_social_media',
        ),
        migrations.RemoveField(
            model_name='yourtipsentry',
            name='hide_real_name',
        ),
        migrations.RemoveField(
            model_name='yourtipsentry',
            name='is_read',
        ),
        migrations.RemoveField(
            model_name='yourtipsentry',
            name='is_shortlisted',
        ),
        migrations.RemoveField(
            model_name='yourtipsentry',
            name='related_article_page',
        ),
        migrations.RemoveField(
            model_name='yourtipsentry',
            name='tip_name',
        ),
        migrations.AddField(
            model_name='yourtipsentry',
            name='user_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='yourtipsentry',
            name='converted_article_page',
            field=models.ForeignKey(blank=True, help_text='Article page to which the entry was converted to', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tip_entries', to='yourtips.YourTipsEntryPage'),
        ),
        migrations.AlterField(
            model_name='yourtipsentry',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
