# -*- coding: utf-8 -*-

from suit_dashboard import DashboardView, Grid, Row, Column, Box, Widget, realtime

from .boxes import MachineUsageBox, MachineInfoBox, MenuBox, RegistrationsBox, LoggedInUsersBox
from .widgets import RandomCurveWidget


class HomeView(DashboardView):
    template_name = 'demo/main.html'
    crumbs = ({'url': 'admin:index', 'name': 'Home'}, )
    grid = Grid(Row(Column(MenuBox())))


class MachineView(HomeView):
    crumbs = ({'url': 'admin:machine', 'name': 'Machine'}, )
    grid = Grid(
        Row(Column(MenuBox())),
        Row(
            Column(MachineInfoBox(), width=6),
            Column(MachineUsageBox(), width=6)))


class UserView(HomeView):
    crumbs = ({'url': 'admin:users', 'name': 'Users'}, )
    grid = Grid(
        Row(
            Column(MenuBox())),
        Row(
            Column(RegistrationsBox(), width=6),
            Column(LoggedInUsersBox(), width=6)))


class DemoView(HomeView):
    crumbs = ({'url': 'admin:demo1', 'name': 'Demo boxes'}, )
    grid = Grid(
        Row(
            Column(MenuBox())),
        Row(
            Column(
                Box(title='Demo paragraph', widgets=[Widget(
                    html_id='paragraph_widget',
                    content='This is an example of paragraph render.',
                    template='demo/paragraph.html')]),
                Box(title='Demo list', widgets=[Widget(
                    html_id='list_widget',
                    content=['This is', 'an example of', 'list render.'],
                    template='demo/list.html')]), width=6),
            Column(
                Box(title='Demo table', widgets=[Widget(
                    html_id='table_widget',
                    content=[
                        ['This', 'is', 'an example'],
                        ['of', 'table', 'render']],
                    template='demo/table.html')]), width=6)))


class RandomCurveView(DemoView):
    crumbs = ({'url': 'admin:curve', 'name': 'Real-time random curve'},)
    grid = Grid(
        Row(Column(MenuBox())),
        Row(Column(Box(widgets=[realtime(RandomCurveWidget())]))))
