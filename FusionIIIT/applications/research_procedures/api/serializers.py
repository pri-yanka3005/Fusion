from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from applications.research_procedures.models import *


class projects_serializer(serializers.ModelSerializer):
    class Meta:
        model = projects
        fields = '__all__'

    def create(self, validated_data):
        return projects.objects.create(**validated_data)
    
class project_access_serializer(serializers.ModelSerializer):
    class Meta:
        model = project_access
        fields = '__all__'

# class requests_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = requests
#         fields = '__all__'


# class requests_serializer(serializers.ModelSerializer):
#     class Meta:
#         model = requests
#         fields = '__all__'

#     def create(self, validated_data):
#         return requests.objects.create(**validated_data)
    
class expenditure_serializer(serializers.ModelSerializer):
    class Meta:
        model = expenditure
        fields = '__all__'

class staff_serializer(serializers.ModelSerializer):
    class Meta:
        model = staff
        fields = '__all__'
