from rest_framework import serializers
from .models import Tasks

class TasksModelSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Tasks.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.save()
        return instance

    class Meta:
        model = Tasks
        fields = '__all__'

class ListTasksModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tasks
        fields = '__all__'