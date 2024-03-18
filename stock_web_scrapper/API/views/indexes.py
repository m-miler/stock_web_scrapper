from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from ..serializers.indexes import IndexesSerializer
from scrapper.models.indexes import Indexes
from ..filters.indexes import IndexesFilters

class IndexesList(ListModelMixin, GenericViewSet):
    queryset = Indexes.objects.all()
    serializer_class = IndexesSerializer
    filterset_class = IndexesFilters

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)