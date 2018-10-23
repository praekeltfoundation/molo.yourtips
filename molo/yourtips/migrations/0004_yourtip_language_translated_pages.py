# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-18 11:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_molo_page'),
        ('yourtips', '0003_add_homepage_action_copy'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='yourtipsarticlepage',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='yourtip',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.SiteLanguage'),
        ),
        migrations.AddField(
            model_name='yourtip',
            name='translated_pages',
            field=models.ManyToManyField(blank=True, related_name='_yourtip_translated_pages_+', to='yourtips.YourTip'),
        ),
    ]