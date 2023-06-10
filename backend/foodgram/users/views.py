from rest_framework import filters, permissions, status, viewsets
from users.models import User
from rest_framework.views import APIView
from api.serializers import UsersSerializer, SignUpSerializer
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    #permission_classes = (permissions.AllowAny,)
    # lookup_field = 'username'
    # filter_backends = (SearchFilter, )
    search_fields = ('username', )
    # http_method_names = ['get', 'post', 'delete', 'patch']
    # Я два дня сижу над этой правкой , ну вообще не могу понять как
    # это сделать , вот что смог . Простите
    # http_method_names = [
    #     m for m in viewsets.ModelViewSet.http_method_names if m not in ['put']]

    @action(
            detail=False, methods=('get', 'post'),
        )
        
    def me(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)


    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        username_taken = User.objects.filter(username=username).exists()
        email_taken = User.objects.filter(email=email).exists()
        if email_taken and not username_taken:
            return Response('email занят', status=status.HTTP_400_BAD_REQUEST)
        if username_taken and not email_taken:
            return Response('username занят',
                            status=status.HTTP_400_BAD_REQUEST)
        user, flag = User.objects.get_or_create(
            username=username,
            email=email)
        # code = default_token_generator.make_token(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)