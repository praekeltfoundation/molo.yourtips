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
)