from rest_framework.serializers import ModelSerializer
from .index_result import IndexResultSerializer
from scrapper.models.indexes import Indexes


class IndexesSerializer(ModelSerializer):
    index_result = IndexResultSerializer(many=True, read_only=True)


    class Meta:
        model = Indexes
        fields = ['ticker', 'index_result']