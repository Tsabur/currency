import django_filters

from rate.models import Rate


class RateFilter(django_filters.FilterSet):
    date = django_filters.NumberFilter(field_name='created', lookup_expr='month')

    class Meta:
        model = Rate
        fields = ['source', 'currency', 'date']
