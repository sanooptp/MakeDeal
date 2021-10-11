from product.models import Product
from django.contrib.auth import mixins
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from restframework import models
from restframework.models import Snippet, TestModel
from restframework.serializers import SnippetSerializer, TestSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from restframework.serializers import UserSerializer
from rest_framework import generics
from rest_framework import permissions
from restframework.permissions import IsOwnerOrReadOnly
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views import generic
from rest_framework.permissions import AllowAny
from .serializers import MyTokenObtainPairSerializer, ProductSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404, redirect


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Test api
class ListTodoAPIView(generics.ListAPIView):
    """This endpoint list all of the available todos from the database"""
    queryset = TestModel.objects.all()
    serializer_class = TestSerializer

class CreateTodoAPIView(generics.CreateAPIView):
    """This endpoint allows for creation of a todo"""
    queryset = TestModel.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UpdateTodoAPIView(generics.UpdateAPIView):
    """This endpoint allows for updating a specific todo by passing in the id of the todo to update"""
    queryset = TestModel.objects.all()
    serializer_class = TestSerializer

class DeleteTodoAPIView(generics.DestroyAPIView):
    """This endpoint allows for deletion of a specific Todo from the database"""
    queryset = TestModel.objects.all()
    serializer_class = TestSerializer


# Authetication 
class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)


class ApitestView(generic.TemplateView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'restframework/apitest.html'

class Apitest(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'restframework/apitestform.html'
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        profile = get_object_or_404(TestModel, pk=pk)
        serializer = TestSerializer(profile)
        return Response({'serializer': serializer, 'profile': profile})

    def post(self, request, pk):
        profile = get_object_or_404(TestModel, pk=pk)
        serializer = TestSerializer(profile, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'profile': profile})
        serializer.save()
        return redirect('apitestlist')

class ApitestListView(generic.ListView):
    template_name= 'restframework/apitestlist.html'
    model= TestModel
    context_object_name= 'profiles'
    

# Login
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

# Proctct View API
class ProductApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    template_name = 'restframework/productview.html'

class ProductView(generic.TemplateView):
    template_name='restframework/productview.html'
    