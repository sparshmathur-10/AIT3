from rest_framework import serializers
from .models import Todo


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'priority', 'status', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # For updates, only update the fields that are provided
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    def validate_title(self, value):
        # Make title optional during updates
        if self.instance is None and not value:
            raise serializers.ValidationError("Title is required when creating a new todo.")
        return value


class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'priority', 'status', 'due_date', 'created_at']


class AIPlanningSerializer(serializers.Serializer):
    tasks = serializers.ListField(
        child=serializers.CharField(max_length=200),
        min_length=1,
        max_length=20
    )
    
    def validate_tasks(self, value):
        if not value or all(not task.strip() for task in value):
            raise serializers.ValidationError("At least one non-empty task is required.")
        return [task.strip() for task in value if task.strip()]


class AIPlanningResponseSerializer(serializers.Serializer):
    plan = serializers.CharField()
    prioritized_tasks = serializers.ListField(child=serializers.DictField()) 