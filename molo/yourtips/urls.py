from django.views.generic import RedirectView

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
        r'^popular-tips/$',
        views.YourTipsPopularView.as_view(),
        name='popular_tips'
    ),
    url(
        r'^tip-share-image/(?P<tip_id>\d+)/$',
        views.ShareImageView.as_view(),
        name='tip_share'
    ),
    url(
        r'^share-tip-on-facebook/(?P<tip_id>\d+)/$',
        views.ShareonFacebookRedirectView.as_view(),
        name='share_tip_on_facebook'),
)
