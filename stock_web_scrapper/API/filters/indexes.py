from django_filters import FilterSet
from scrapper.models.indexes import Indexes


class IndexesFilters(FilterSet):
    class Meta:
        model = Indexes
        fields = ["ticker"]
