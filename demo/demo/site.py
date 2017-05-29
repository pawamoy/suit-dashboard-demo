# -*- coding: utf-8 -*-

from django.contrib.admin.sites import AdminSite
from django.conf.urls import url

from suit_dashboard.urls import get_realtime_urls

from .views import HomeView, MachineView, UserView, DemoView, RandomCurveView


class DashboardSite(AdminSite):
    """A Django AdminSite to allow registering custom dashboard views."""

    def get_urls(self):
        urls = super(DashboardSite, self).get_urls()
        custom_urls = [
            url(r'^$', self.admin_view(HomeView.as_view()), name='index'),
            url(r'^machine/$', self.admin_view(MachineView.as_view()), name='machine'),
            url(r'^users/$', self.admin_view(UserView.as_view()), name='users'),
            url(r'^demo1/$', self.admin_view(DemoView.as_view()), name='demo1'),
            url(r'^demo1/demo1a/$', self.admin_view(RandomCurveView.as_view()), name='curve'),
        ]

        del urls[0]
        return custom_urls + get_realtime_urls(self.admin_view) + urls
