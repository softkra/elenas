from rest_framework.response import Response
from . models import *
from rest_framework.views import APIView
from . serializers import TasksModelSerializer, ListTasksModelSerializer
from django.core import serializers
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.authtoken.models import Token

""" MODULE: USER """

"""
    Class to create user system
"""
class CreateUserAPIView(APIView):
    serializer_class = None
    permission_classes = (AllowAny,)
    def post(self,request):
        """
            POST Method. Params: data: {username: Username, email: Email user, password: Password user}
        """
        try:
            user = User.objects.create_user(
                request.data['username'],
                request.data['email'],
                request.data['password']
            )
            return Response("User added successfully", status.HTTP_201_CREATED)
        except MultiValueDictKeyError:
            return Response("Error adding the user", status.HTTP_500_INTERNAL_SERVER_ERROR)
        except IntegrityError:
            return Response("Database error adding the user", status.HTTP_500_INTERNAL_SERVER_ERROR)



""" MODULE: TASKS """

"""
    Class to create task record
"""
class CreateTaskAPIView(APIView):
    """
        POST Method
        Params:
            data: {
                name: Task name
                description: Task description
                attribute: Task attribute
            }
    """
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            data = get_user_by_token(request)

            serializer = TasksModelSerializer(data = data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        except MultiValueDictKeyError:
            return Response("Error adding the task", status.HTTP_500_INTERNAL_SERVER_ERROR)
        except IntegrityError:
            return Response("Database error adding the task", status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
    Class to update task record
"""
class UpdateTaskAPIView(UpdateAPIView):
    """
        PUT Method
        Params:
            pk: Task_id
            data: {
                name: Task name
                description: Task description
                attribute: Task attribute
            }
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TasksModelSerializer
    def update(self,request,pk):
        try:
            task = Tasks.objects.get(id=pk)
            data = get_user_by_token(request)
            serializer = self.get_serializer(task, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("task Does not exist", status.HTTP_200_OK)
        except MultiValueDictKeyError:
            return Response("Error updating the task", status.HTTP_404HTTP_500_INTERNAL_SERVER_ERROR_NOT_FOUND)
        except IntegrityError:
            return Response("Database error updating the task", status.HTTP_500_INTERNAL_SERVER_ERROR)

"""
    Class to show detail task record
"""
class DetailTaskAPIView(APIView):
    """
        GET Method
        Params:
            pk: task_id
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        result = Tasks.objects.filter(id=pk)
        serializer = TasksModelSerializer(result, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

"""
    Class to delete task record
"""
class DeleteTaskAPIView(APIView):
    """
        DELETE Method
        Params:
            pk: task_id
    """
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            result = Tasks.objects.get(id=pk)
            result.delete()
            return Response("task deleted successfully", status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("task Does not Exist", status.HTTP_404_NOT_FOUND)

"""
    Class to partial update task record
"""
class ChangeStatusTaskAPIView(UpdateAPIView):
    """
        PATCH Method
        Params:
            pk: Task_id
    """
    permission_classes = [IsAuthenticated]
    serializer_class = TasksModelSerializer
    def update(self,request,pk):
        try:
            task = Tasks.objects.get(id=pk)
            serializer = self.get_serializer(
                task,
                data={"is_completed": request.data.get('is_completed', task.is_completed)},
                partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response("task Does not exist", status.HTTP_200_OK)
        except MultiValueDictKeyError:
            return Response("Error updating the task", status.HTTP_404HTTP_500_INTERNAL_SERVER_ERROR_NOT_FOUND)
        except IntegrityError:
            return Response("Database error updating the task", status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListTaskAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        queryset = Tasks.objects.filter(user=request.user.id).order_by("id")
        page = self.paginate_queryset(queryset)
        serializer_context = {'request': request}
        serializer = TasksModelSerializer(
            page, context=serializer_context, many=True
        )
        return self.get_paginated_response(serializer.data)

class SearchTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, search=None):
        queryset = Tasks.objects.filter(user=request.user.id, description__icontains=search)
        serializer = TasksModelSerializer(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

def get_user_by_token(request):
    data = request.data
    if type(data) is dict:
        data['user'] = request.user.id
    else:
        mutable = data._mutable
        data._mutable = True
        data["user"] = request.user.id
        data._mutable = mutable
    return data
