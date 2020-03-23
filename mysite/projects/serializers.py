from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('__all__')


class ProjectCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("title", "description", "technology", "coordinator",
                  "coordinator_email", "link", "is_approved")


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("image",)
