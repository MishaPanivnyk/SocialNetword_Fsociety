from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Friend
from .serializers import FriendSerializer

class FriendListView(APIView):
    def get(self, request):
        friends = Friend.objects.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)
