from backend.models import Awards
from backend.api.serializers import AwardsSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

serializers = AwardsSerializer(Awards.objects.all(),many=True)
serializers.data
