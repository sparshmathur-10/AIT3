import requests
import json
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import Todo
from .serializers import (
    TodoSerializer, 
    TodoListSerializer, 
    AIPlanningSerializer,
    AIPlanningResponseSerializer
)


class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TodoListSerializer
        return TodoSerializer
    
    @action(detail=False, methods=['post'])
    def plan(self, request):
        """
        AI Planning endpoint using DeepSeek API
        """
        serializer = AIPlanningSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        tasks = serializer.validated_data['tasks']
        
        try:
            # Prepare prompt for DeepSeek API
            prompt = f"""You are now PlanningProductivityExpert. Make a realistic plan based on priority and length of these tasks:

Tasks:
{chr(10).join(f"- {task}" for task in tasks)}

Please provide:
1. A comprehensive plan with estimated time for each task
2. Priority recommendations (High/Medium/Low)
3. Suggested order of execution
4. Any dependencies between tasks

Format your response as JSON with the following structure:
{{
    "plan": "Your detailed planning advice here",
    "prioritized_tasks": [
        {{
            "task": "task description",
            "priority": "high/medium/low",
            "estimated_time": "X hours/minutes",
            "order": 1
        }}
    ]
}}"""

            # Call DeepSeek API via GitHub
            headers = {
                'Authorization': f'token {settings.GITHUB_TOKEN}',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json',
            }
            
            # Using GitHub's API to access DeepSeek (this is a placeholder - you'll need to adjust based on actual API)
            # For now, we'll simulate the response
            response_data = {
                "plan": f"Based on the {len(tasks)} tasks provided, here's a comprehensive plan:\n\n" +
                       "1. **High Priority Tasks**: Focus on urgent and important items first\n" +
                       "2. **Time Management**: Allocate realistic time blocks for each task\n" +
                       "3. **Dependencies**: Consider task dependencies and prerequisites\n" +
                       "4. **Flexibility**: Build in buffer time for unexpected issues\n\n" +
                       "Recommended approach: Start with quick wins to build momentum, then tackle complex tasks.",
                "prioritized_tasks": [
                    {
                        "task": task,
                        "priority": "high" if i < len(tasks) // 3 else "medium" if i < 2 * len(tasks) // 3 else "low",
                        "estimated_time": f"{30 + i * 15} minutes",
                        "order": i + 1
                    }
                    for i, task in enumerate(tasks)
                ]
            }
            
            # In production, replace the above with actual API call:
            # response = requests.post(
            #     'https://api.github.com/...',  # DeepSeek API endpoint
            #     headers=headers,
            #     json={'prompt': prompt}
            # )
            # response_data = response.json()
            
            response_serializer = AIPlanningResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Invalid response format from AI service'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
                
        except requests.RequestException as e:
            return Response(
                {'error': f'Failed to connect to AI service: {str(e)}'}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            return Response(
                {'error': f'AI planning failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 