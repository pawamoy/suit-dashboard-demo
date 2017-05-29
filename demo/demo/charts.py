# -*- coding: utf-8 -*-

import os

from django.utils.translation import ugettext as _

import psutil

from .stats import member_registration_stats


def machine_usage_chart(series_only=False):
    # Retrieve some raw data
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()

    statvfs = os.statvfs('/')

    total_space = statvfs.f_frsize * statvfs.f_blocks
    free_space = statvfs.f_frsize * statvfs.f_bfree
    used_space = (total_space - free_space) / total_space * 100

    # Green, orange, red or grey color for usage/idle
    green, orange, red, grey = '#00FF38', '#FFB400', '#FF3B00', '#EBEBEB'

    ram_color = green  # default
    if ram >= 75:
        ram_color = red
    elif ram >= 50:
        ram_color = orange

    cpu_color = green
    if cpu >= 75:
        cpu_color = red
    elif cpu >= 50:
        cpu_color = orange

    disk_color = green
    if used_space >= 75:
        disk_color = red
    elif used_space >= 50:
        disk_color = orange

    series = [{
        'name': _('CPU idle'),
        'data': [{'y': 100 - cpu, 'color': grey}, {'y': 0}, {'y': 0}],
    }, {
        'name': _('CPU used'),
        'data': [{'y': cpu, 'color': cpu_color}, {'y': 0}, {'y': 0}],
    }, {
        'name': _('RAM free'),
        'data': [{'y': 0}, {'y': 100 - ram, 'color': grey}, {'y': 0}],
    }, {
        'name': _('RAM used'),
        'data': [{'y': 0}, {'y': ram, 'color': ram_color}, {'y': 0}],
    }, {
        'name': _('Disk free'),
        'data': [{'y': 0}, {'y': 0}, {'y': 100 - used_space, 'color': grey}],
    }, {
        'name': _('Disk used'),
        'data': [{'y': 0}, {'y': 0}, {'y': used_space, 'color': disk_color}],
    }]

    if series_only:
        return series

    # Now create a chart to display CPU and RAM usage
    chart_options = {
        'chart': {
            'type': 'bar',
            'height': 200
        },
        'title': {
            'text': _('CPU, RAM and Disk usage')
        },
        'xAxis': {
            'categories': [_('CPU usage'), _('RAM usage'), _('Disk usage')]
        },
        'yAxis': {
            'min': 0,
            'max': 100,
            'title': {
                'text': _('Percents')
            }
        },
        'tooltip': {
            'percentageDecimals': 1
        },
        'legend': {
            'enabled': False
        },
        'plotOptions': {
            'series': {
                'stacking': 'normal'
            }
        },
        'series': series
    }

    return chart_options


def member_registration_chart(queryset=None):
    stats = member_registration_stats(queryset=queryset)

    chart = {
        'chart': {
            'type': 'area',
            'zoomType': 'x'
        },
        'title': {
            'text': '',
        },
        'xAxis': {
            'type': 'datetime',
        },
        'yAxis': {
            'title': {
                'text': _('Nb registration')
            }
        },
        'legend': {
            'enabled': True
        },
        'tooltip': {
            'shared': True,
            'valueDecimals': 2
        },
        'plotOptions': {
            'area': {
                'marker': {
                    'enabled': False,
                    'symbol': 'circle',
                    'radius': 2,
                    'states': {
                        'hover': {
                            'enabled': True
                        }
                    }
                }
            }
        },
        'series': []
    }

    chart['series'].append({'name': _('Registrations that day'), 'data': stats['data']})
    chart['series'].append({'name': _('Registrations sum'), 'data': stats['data_summed']})

    return chart
