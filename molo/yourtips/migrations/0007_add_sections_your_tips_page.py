# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_yourtips_index(apps, schema_editor):
    from molo.core.models import Main, SectionPage, SectionIndexPage
    from molo.yourtips.models import (
        YourTipsIndexPage, YourTipsArticleIndexPage, YourTipsPage
    )
    main = Main.objects.all().first()

    if main:
        tip_index = YourTipsIndexPage.objects.get(
            title='Tips', slug='tips'
        )
        tip_article_index = YourTipsArticleIndexPage(
            title='Read Tips', slug='read-tips'
        )
        tip_index.add_child(instance=tip_article_index)
        tip_article_index.save_revision().publish()
        tip_page = YourTipsPage(
            title='Your Tips Page',
            description='Your Tips page',
            slug='your-tips-page')
        tip_index.add_child(instance=tip_page)
        tip_page.save_revision().publish()
        tip_index.save()
        section = SectionPage(
            title='Your tips',
            slug='your-tips'
        )
        section_index = SectionIndexPage.objects.get(
            title='Sections', slug='sections'
        )
        section_index.add_child(instance=section)
        section.save_revision().publish()



class Migration(migrations.Migration):

    dependencies = [
        ('yourtips', '0006_auto_20170626_1448'),
    ]

    operations = [
        migrations.RunPython(create_yourtips_index),
    ]
