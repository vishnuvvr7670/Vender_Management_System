from rest_framework import serializers

from venders.models import *

class VenderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=VenderModel
        fields='__all__'
