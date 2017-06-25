# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_sections(apps, schema_editor):
    from molo.core.models import Main, SectionPage
    from molo.yourtips.models import (
        YourTipsArticleIndexPage
    )
    main = Main.objects.all().first()

    if main:
        section = SectionPage(
            title='Your Tips',
            slug='your-tips'
        )
        main.add_child(instance=section)
        section.save_revision().publish()
        tip_article_index = YourTipsArticleIndexPage.objects.get(
            title='Read Tips', slug='read-tips'
        )
        section.add_child(instance=tip_article_index)
        section.save_revision().publish()


class Migration(migrations.Migration):

    dependencies = [
        ('yourtips', '0006_create_your_tip_article_index_pages'),
    ]

    operations = [
        migrations.RunPython(create_sections),
    ]
