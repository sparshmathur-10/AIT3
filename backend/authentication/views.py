import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import GoogleAuthSerializer, AuthResponseSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def google_auth(request):
    """
    Authenticate user with Google OAuth token
    """
    print(f"Received request data: {request.data}")  # Debug log
    
    serializer = GoogleAuthSerializer(data=request.data)
    if not serializer.is_valid():
        print(f"Serializer errors: {serializer.errors}")  # Debug log
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    token = serializer.validated_data['token']
    print(f"Token received: {token[:20]}...")  # Debug log
    
    try:
        # Verify the token with Google
        google_response = requests.get(
            'https://www.googleapis.com/oauth2/v3/tokeninfo',
            params={'access_token': token}
        )
        
        if google_response.status_code != 200:
            return Response(
                {'error': 'Invalid Google token'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user_info = google_response.json()
        
        # Check if the token is for our app
        # Temporarily disabled for testing
        # if user_info.get('aud') != settings.GOOGLE_CLIENT_ID:
        #     return Response(
        #         {'error': 'Invalid client ID'}, 
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        
        google_id = user_info.get('sub')
        email = user_info.get('email')
        name = user_info.get('name', '')
        picture = user_info.get('picture', '')
        
        # Get or create user
        user, created = User.objects.get_or_create(
            google_id=google_id,
            defaults={
                'email': email,
                'username': email,
                'first_name': name.split()[0] if name else '',
                'last_name': ' '.join(name.split()[1:]) if name and len(name.split()) > 1 else '',
                'profile_picture': picture,
            }
        )
        
        # Update user info if not newly created
        if not created:
            user.email = email
            user.first_name = name.split()[0] if name else user.first_name
            user.last_name = ' '.join(name.split()[1:]) if name and len(name.split()) > 1 else user.last_name
            user.profile_picture = picture
            user.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        response_data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'profile_picture': user.profile_picture,
            },
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except requests.RequestException:
        return Response(
            {'error': 'Failed to verify Google token'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 