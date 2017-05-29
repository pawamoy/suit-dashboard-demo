# -*- coding: utf-8 -*-

import json
import platform
import random
from datetime import datetime, timedelta

from django.utils import timezone
from suit_dashboard import Widget

from .charts import member_registration_chart, machine_usage_chart


class RandomCurveWidget(Widget):
    html_id = 'random_curve_widget'
    name = 'Random Curve Widget'
    template = 'demo/random_curve.html'
    url_name = 'random_curve'
    url_regex = 'realtime/random_curve'
    max_points = 30
    time_interval = 1000

    # initial content
    content = json.dumps({
        'chart': {
            'type': 'spline',
            'marginRight': 10,
        },
        'title': {
            'text': 'Live random data'
        },
        'xAxis': {
            'type': 'datetime',
            'tickPixelInterval': 150
        },
        'yAxis': {
            'title': {
                'text': 'Value'
            },
            'plotLines': [{
                'value': 0,
                'width': 1,
                'color': '#808080'
            }]
        },
        'series': [{
            'name': 'Random data',
            'data': []
        }]
    })

    # get random points
    def get_updated_content(self):
        return (
            (timezone.make_aware(
                datetime.now(), timezone.get_current_timezone()
            ) - timezone.make_aware(
                datetime(1970, 1, 1),
                timezone.get_current_timezone()
            )).total_seconds() * 1000.0,
            random.choice(range(0, 25)),
        )


class MachineInfoWidget(Widget):
    html_id = 'sysspec'
    name = 'System specifications'
    template = 'demo/table.html'
    classes = 'table-bordered table-condensed table-hover table-striped'

    @property
    def content(self):
        with open('/proc/uptime') as f:
            s = timedelta(seconds=float(f.readline().split()[0])).total_seconds()  # NOQA
            uptime = '%d days, %d hours, %d minutes, %d seconds' % (
                s // 86400, s // 3600 % 24, s // 60 % 60, s % 60)

        return (
            ('Hostname', platform.node()),
            ('System', '%s, %s, %s' % (
                platform.system(),
                ' '.join(platform.linux_distribution()),
                platform.release())),
            ('Architecture', ' '.join(platform.architecture())),
            ('Processor', platform.processor()),
            ('Python version', platform.python_version()),
            ('Uptime', uptime)
        )


class MachineUsageWidget(Widget):
    html_id = 'highchart-machine-usage'
    content = json.dumps(machine_usage_chart())
    template = 'demo/machine_usage.html'

    def get_updated_content(self):
        return machine_usage_chart(series_only=True)


class MemberRegistrations(Widget):
    html_id = 'chart-registrations'
    template = 'demo/highchart.html'

    @property
    def content(self):
        # this one is a property to avoid "no such table" error at migrate
        return json.dumps(member_registration_chart())
