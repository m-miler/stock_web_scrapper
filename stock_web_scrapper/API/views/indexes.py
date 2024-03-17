from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from ..serializers.indexes import IndexesSerializer
from scrapper.models.indexes import Indexes

class IndexesList(ListModelMixin, GenericViewSet):
    queryset = Indexes.objects.all()
    serializer_class = IndexesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)