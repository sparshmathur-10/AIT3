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
        AI Planning endpoint using GitHub AI inference API with DeepSeek model
        """
        serializer = AIPlanningSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        tasks = serializer.validated_data['tasks']
        
        try:
            # Prepare prompt for AI planning
            system_prompt = """You are a productivity expert. Analyze the given tasks and provide a comprehensive plan with:
1. A detailed planning strategy
2. Prioritized task list with estimated time and priority levels
3. Suggested execution order
4. Any dependencies or recommendations

Format your response as JSON with this structure:
{
    "plan": "Your detailed planning advice here",
    "prioritized_tasks": [
        {
            "task": "task description",
            "priority": "high/medium/low",
            "estimated_time": "X hours/minutes",
            "order": 1
        }
    ]
}"""

            user_prompt = f"""Please analyze and plan these {len(tasks)} tasks:

{chr(10).join(f"- {task}" for task in tasks)}

Provide a realistic, actionable plan that considers task complexity, dependencies, and optimal execution order."""

            # Call GitHub AI inference API
            headers = {
                'Authorization': f'Bearer {settings.GITHUB_TOKEN}',
                'Content-Type': 'application/json',
            }
            
            payload = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2048,
                "model": "deepseek/DeepSeek-V3-0324"
            }
            
            response = requests.post(
                'https://models.github.ai/inference/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                return Response(
                    {'error': f'AI service error: {response.status_code} - {response.text}'}, 
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            
            ai_response = response.json()
            content = ai_response.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Try to parse JSON from the response
            try:
                # Extract JSON from the response (it might be wrapped in markdown)
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    response_data = json.loads(json_match.group())
                else:
                    # Fallback: create a structured response from the text
                    response_data = {
                        "plan": content,
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
            except json.JSONDecodeError:
                # If JSON parsing fails, create a structured response
                response_data = {
                    "plan": content,
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