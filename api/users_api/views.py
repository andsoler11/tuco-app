from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    """ Vista de creacion de usuario """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()



class UserListView(generics.ListAPIView):
    """ Vista de listado de usuarios """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):

        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """ Vista de detalle de usuario """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        serializer = self.get_serializer(user)


        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        user = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        serializer = self.get_serializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)