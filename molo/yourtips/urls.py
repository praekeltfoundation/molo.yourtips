from molo.yourtips import views

from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(
        r'^entry/(?P<slug>[\w-]+)/$',
        views.YourTipsEntryView.as_view(),
        name='tip_entry'),

    url(
        r'^thankyou/(?P<slug>[\w-]+)/$',
        views.ThankYouView.as_view(),
        name='thank_you'),
    url(
        r'^recent-tips/$',
        views.YourTipsRecentView.as_view(),
        name='recent_tips'
    ),
    url(
        r'^recent-tips-index/$',
        'molo.yourtips.views.recent_tips_index',
        name='recent_tips_index'
    )
)
