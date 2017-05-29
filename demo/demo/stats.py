# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.contrib.auth import get_user_model


def ms_since_epoch(dt):
    return (dt - datetime(1970, 1, 1).date()).total_seconds() * 1000


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def member_registration_stats(queryset=None):
    if queryset is None:
        user = get_user_model()
        queryset = user.objects.all()
    start_date = datetime.date(queryset.order_by('date_joined')[0].date_joined)
    end_date = datetime.now().date()

    data = {d: 0 for d in daterange(start_date, end_date)}
    for m in queryset:
        d = m.date_joined.date()
        if data.get(d, None) is None:
            data[d] = 0
        data[d] += 1
    data = sorted([(ms_since_epoch(dj), r) for dj, r in data.items()])

    s = 0
    data_summed = []
    for d in data:
        s += d[1]
        data_summed.append((d[0], s))

    first_day = timedelta(milliseconds=data[0][0])
    last_day = timedelta(milliseconds=data[-1][0])
    first_nb = data[0][1]
    nb_reg = queryset.count()
    data_average_per_day = [(data_summed[0][0], 0.0)]
    data_average_per_day_since_date = []
    for d in data_summed[1:]:
        data_average_per_day.append(
            (d[0], (d[1] - first_nb) / (timedelta(milliseconds=d[0]) - first_day).days))
    for d in data_summed[:-1]:
        data_average_per_day_since_date.append(
            (d[0], (nb_reg - d[1]) / (last_day - timedelta(milliseconds=d[0])).days))

    return {
        'data': data,
        'data_summed': data_summed,
        'data_average_per_day_since_date': data_average_per_day_since_date,
        'data_average_per_day': data_average_per_day,
    }
