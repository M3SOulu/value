import operator

from django.db.models import Count

from value.factors.models import Factor
from value.deliverables.meetings.models import Meeting, MeetingItem, Evaluation


class Highcharts(object):

    label_style = { 'fontSize': '13px', 'fontFamily': '"Helvetica Neue", Helvetica, Arial, sans-serif' }

    def feature_comparison_pie_chart(self, meeting, measure_value):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting)
        filtered_evaluations = evaluations.filter(measure_value=measure_value)

        vqs = filtered_evaluations.values('meeting_item__id', 'meeting_item__decision_item__name').annotate(count=Count('meeting_item__id')).order_by('-count')

        data = []
        for result in vqs:
            data.append([result['meeting_item__decision_item__name'], result['count']])

        options = {
            'chart': { 'type': 'column' },
            'title': { 'text': None },
            'xAxis': {
                'type': 'category',
                'labels': {
                    'rotation': -45,
                    'style': { 'fontSize': '13px', 'fontFamily': 'Verdana, sans-serif' }
                }
            },
            'yAxis': { 'min': 0, 'title': { 'text': measure_value.description + ' votes' }},
            'legend': { 'enabled': False },
            'tooltip': { 'pointFormat': 'Overall ' + measure_value.description.lower() + ' votes: <strong>{point.y}</strong>' },
            'series': [{
                'name': measure_value.description + ' Votes',
                'data': data,
                'color': measure_value.color,
                'dataLabels': {
                    'enabled': True,
                    'rotation': -90,
                    'color': '#FFFFFF',
                    'align': 'right',
                    'format': '{point.y}',
                    'y': 10,
                    'style': self.label_style
                }
            }]
        }

        return options


    def stakeholders_input_bar_chart(self, meeting):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting)
        meeting_stakeholders = meeting.meetingstakeholder_set.all()
        factors = Factor.get_factors()

        data = []

        meeting_items_count = meeting.meetingitem_set.count()
        factors_count = factors.count()

        max_input = factors_count * meeting_items_count

        for meeting_stakeholder in meeting_stakeholders:
            votes = evaluations.filter(user=meeting_stakeholder.stakeholder).count()
            if max_input != 0:
                percentage = round((votes / float(max_input)) * 100.0, 2)
            else:
                percentage = 0.0
            data.append([meeting_stakeholder.stakeholder.profile.get_display_name(), percentage])

        data = sorted(data, key=operator.itemgetter(1))
        data.reverse()

        options = {
            'chart': { 'type': 'bar' },
            'title': { 'text': None },
            'xAxis': {
                'type': 'category',
                'labels': { 'style': self.label_style }
            },
            'yAxis': { 'min': 0, 'max': 100, 'title': { 'text': 'Stakeholder Meeting Input' }},
            'legend': { 'enabled': False },
            'tooltip': { 'pointFormat': 'Usage percentage: <strong>{point.y}%</strong>' },
            'series': [{
                'name': 'Stakeholder Meeting Input',
                'data': data,
                'color': '#337AB7',
                'dataLabels': {
                    'enabled': True,
                    'color': '#FFFFFF',
                    'align': 'right',
                    'format': '{point.y}%',
                    'style': self.label_style
                }
            }]
        }

        return options


    def factors_usage_bar_chart(self, meeting):
        evaluations = Evaluation.get_evaluations_by_meeting(meeting)
        factors = Factor.get_factors()
        data = []

        meeting_items_count = meeting.meetingitem_set.count()
        stakeholders_count = meeting.meetingstakeholder_set.count()

        max_votes = stakeholders_count * meeting_items_count

        for factor in factors:
            votes = evaluations.filter(factor=factor).exclude(measure_value__description='N/A').count()
            if max_votes != 0:
                percentage = round((votes / float(max_votes)) * 100.0, 2)
            else:
                percentage = 0.0
            data.append([factor.name, percentage])

        data = sorted(data, key=operator.itemgetter(1))
        data.reverse()

        options = {
            'chart': { 'type': 'column' },
            'title': { 'text': None },
            'xAxis': {
                'type': 'category',
                'labels': { 'style': self.label_style }
            },
            'yAxis': { 'min': 0, 'max': 100, 'title': { 'text': 'Factors usage percentage' }},
            'legend': { 'enabled': False },
            'tooltip': { 'pointFormat': 'Usage percentage: <strong>{point.y}%</strong>' },
            'series': [{
                'name': 'Factors usage percentage',
                'data': data,
                'color': '#337AB7',
                'dataLabels': {
                    'enabled': True,
                    'rotation': -90,
                    'color': '#FFFFFF',
                    'align': 'right',
                    'format': '{point.y}%',
                    'y': 10,
                    'style': self.label_style
                }
            }]
        }

        return options

    def features_selection_stacked_chart(self, meeting_id, meeting_item_id, chart):
        
        chart_type = 'bar'
        stacking = None

        if chart in ['stacked_bars', 'stacked_columns',]:
            stacking = 'normal'

        if chart in ['stacked_columns', 'basic_columns',]:
            chart_type = 'column'

        meeting = Meeting.objects.get(pk=meeting_id)
        meeting_item = MeetingItem.objects.get(pk=meeting_item_id)
        evaluations = Evaluation.get_evaluations_by_meeting(meeting).filter(meeting_item=meeting_item)

        if evaluations:
            data = {}

            for evaluation in evaluations:
                data[evaluation.factor.name] = {}
                for value in evaluation.factor.measure.measurevalue_set.all():
                    data[evaluation.factor.name][value.description] = 0

            for evaluation in evaluations:
                data[evaluation.factor.name][evaluation.measure_value.description] = data[evaluation.factor.name][evaluation.measure_value.description] + 1

            sorted_data = sorted(data.items(), key=operator.itemgetter(0))

            categories = []
            for factor in sorted_data:
                categories.append(factor[0])

            measure = evaluations[0].measure

            series = []
            for value in measure.measurevalue_set.all():
                serie_data = []
                for factor in sorted_data:
                    serie_data.append(factor[1][value.description])
                series.append({ 'name': value.description, 'data': serie_data, 'color': value.color })

            options = {
                'chart': { 'type': chart_type },
                'title': { 'text': '' },
                'xAxis': { 'categories': categories },
                'yAxis': { 'min': 0, 'title': { 'text': 'Number of votes' } },
                'legend': { 'reversed': True },
                'plotOptions': { 'series': { 'stacking': stacking }},
                'series': series
            }

        else:
            options = {}

        return options

    def _base_treemap(self, data):
        options = {
            'series': [{
                'type': 'treemap',
                'layoutAlgorithm': 'stripes',
                'alternateStartingDirection': True,
                'levels': [{
                    'level': 1,
                    'layoutAlgorithm': 'sliceAndDice',
                    'dataLabels': {
                        'enabled': True,
                        'align': 'left',
                        'verticalAlign': 'top',
                        'style': { 'fontSize': '15px', 'fontWeight': 'bold' }
                    }
                }],
                'data': data
            }],
            'title': { 'text': '' }
        }
        return options

    def features_acceptance_simple_treemap(self, instance_id, item_id):
        instance = Meeting.objects.get(pk=instance_id)
        item = MeetingItem.objects.get(pk=item_id)
        evaluations = Evaluation.get_evaluations_by_meeting(instance).filter(meeting_item=item)

        vqs = evaluations.values('measure_value__description', 'measure_value__color').annotate(value=Count('measure_value__description')).order_by()
        data = [kv for kv in vqs]
        for d in data:
            d['name'] = d.pop('measure_value__description')
            d['color'] = d.pop('measure_value__color')

        return self._base_treemap(data)

    def features_acceptance_detailed_treemap(self, instance_id, item_id):
        instance = Meeting.objects.get(pk=instance_id)
        item = MeetingItem.objects.get(pk=item_id)
        evaluations = Evaluation.get_evaluations_by_meeting(instance).filter(meeting_item=item)

        vqs = evaluations.order_by('measure_value__description', 'measure_value__id', 'measure_value__color').distinct('measure_value__description', 'measure_value__id', 'measure_value__color').values('measure_value__description', 'measure_value__id', 'measure_value__color')
        groups = [kv for kv in vqs]
        for g in groups:
            g['id'] = g['measure_value__description']
            g['name'] = g['measure_value__description']
            del g['measure_value__description']
            g['color'] = g.pop('measure_value__color')

        vqs = evaluations.values('measure_value__description', 'factor__name').annotate(value=Count('measure_value__description')).order_by()
        data = [kv for kv in vqs]
        for d in data:
            d['name'] = d.pop('factor__name')
            d['parent'] = d.pop('measure_value__description')

        data = groups + data

        return self._base_treemap(data)

    def features_acceptance_pie_chart_drilldown(self, instance_id, item_id):
        instance = Meeting.objects.get(pk=instance_id)
        item = MeetingItem.objects.get(pk=item_id)
        evaluations = Evaluation.get_evaluations_by_meeting(instance).filter(meeting_item=item)

        vqs = evaluations.values('measure_value__description', 'measure_value__color').annotate(y=Count('measure_value__description')).order_by('y')
        series = [kv for kv in vqs]
        for serie in series:
            serie['name'] = serie['measure_value__description']
            serie['drilldown'] = serie['measure_value__description']
            del serie['measure_value__description']
            serie['color'] = serie.pop('measure_value__color')

        vqs = evaluations.order_by('measure_value__id', 'measure_value__description').distinct('measure_value__id', 'measure_value__description').values('measure_value__id', 'measure_value__description')

        drilldownSeries = []

        for v in vqs:
            vqs = evaluations.filter(measure_value__id=v['measure_value__id']).values('measure_value__description', 'factor__name').annotate(y=Count('measure_value__description')).order_by('y')
            data = []
            for value in vqs:
                data.append([value['factor__name'], value['y']])

            drilldown = {
                'data': data,
                'id': v['measure_value__description'],
                'name': v['measure_value__description']
            }

            drilldownSeries.append(drilldown)

        options = {
                'chart': { 'type': 'pie' },
                'title': { 'text': '' },
                'subtitle': { 'text': 'Stakeholders opinion. Click the slices to view value factors.' },
                'plotOptions': { 'series': { 'dataLabels': { 'enabled': True, 'format': '{point.name}: {point.y} votes' } } },
                'tooltip': {
                    'headerFormat': '<span style="font-size:11px">{series.name}</span><br>',
                    'pointFormat': '<span style="color:{point.color}">{point.name}</span>: <b>{point.y}</b><br/>'
                },
                'series': [{
                    'name': 'Votes',
                    'colorByPoint': True,
                    'data': series
                }],
                'drilldown': {
                    'series': drilldownSeries
                }
            }
        return options
