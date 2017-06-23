# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def create_yourtips_index(apps, schema_editor):
    from molo.core.models import Main
    from molo.yourtips.models import (
        YourTipsIndexPage, YourTipsArticleIndexPage, YourTips
    )
    main = Main.objects.all().first()

    if main:
        tip_index = YourTipsIndexPage.objects.get(
            title='Your tips', slug='your-tips'
        )
        tip_article_index = YourTipsArticleIndexPage(
            title='Read Tips', slug='read-your-tips'
        )
        tip_index.add_child(instance=tip_article_index)
        tip_article_index.save_revision().publish()
        tip = YourTips(
            title='Tips',
            description='Your Tip page',
            slug='tips')
        tip_index.add_child(instance=tip)
        tip.save_revision().publish()
        tip_index.save()


class Migration(migrations.Migration):

    dependencies = [
        ('yourtips', '0005_auto_20170623_0804'),
    ]

    operations = [
        migrations.RunPython(create_yourtips_index),
    ]
1