from rest_framework.serializers import ModelSerializer
from scrapper.models.indexes import IndexResult


class IndexResultSerializer(ModelSerializer):
    class Meta:
        model = IndexResult
        fields = '__all__'

