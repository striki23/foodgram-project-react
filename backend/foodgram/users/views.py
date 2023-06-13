from rest_framework import filters, permissions, status, viewsets
from users.models import User, Subscribe
from rest_framework.views import APIView
from api.serializers import CustomUserSerializer, SubscribeSerializer
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    search_fields = ('username', )
    permission_classes = (permissions.AllowAny,)

    @action(
            detail=False, methods=('get', 'post'),
        )
        
    def me(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class SubscribeViewSet(viewsets.ModelViewSet):
    #queryset = User.objects.all()
    #serializer_class = UsersSerializer
    
    @action(url_path='subscriptions', methods=['get'], detail=False,
            #permission_classes=[IsAuthenticated]
        )
    
    def subscriptions(self, request):
        user = self.request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)