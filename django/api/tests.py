import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from api.models import Tasks
from api.serializers import ListTasksModelSerializer, TasksModelSerializer
USER_DATA = {
    "username": "superuser",
    "email": "prueba@gmail.com",
    "password": "superpass"
}
class RegistrationUserTestCase(APITestCase):
    def test_registration(self):
        response = self.client.post("/api/registration/", USER_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class UserTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USER_DATA["username"], password=USER_DATA["password"])
        #self.token = Token.objects.create(user=self.user)
        #self.client.credentials(HTTP_AUTHORIZATION="Token "+ self.token)

    def test_login(self):
        data = {
            "username":USER_DATA["username"], 
            "password":USER_DATA["password"]
        }
        response = self.client.post("/authentication/login/", data)
        token = Token.objects.filter(user=self.user).exists()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(True, token)

TASK_DATA = {
    "title": "Alarma",
    "description": "Alarma de las 8 AM" 
}
class TasksTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username=USER_DATA["username"], password=USER_DATA["password"])
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token {}".format( self.token))
        self.task = Tasks(
            title=TASK_DATA['title'],
            description=TASK_DATA['description'],
            user=self.user
        )
        self.task.save()

    def test_list_tasks(self):
        response = self.client.get("/api/list-task/")
        json_response = response.json()
        count = Tasks.objects.filter(user=self.user).count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], count)
    
    def test_search_by_description(self):
        response = self.client.get("/api/search-task/alarma/")
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_task(self):
        response = self.client.post("/api/add-task/", TASK_DATA)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_update_task(self):
        response = self.client.put("/api/update-task/{}/".format(self.task.id), TASK_DATA)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_detail_task(self):
        response = self.client.get("/api/detail-task/{}/".format(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_delete_task(self):
        response = self.client.delete("/api/delete-task/{}/".format(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_task(self):
        response = self.client.put("/api/change-task/{}/".format(self.task.id), {"is_completed": True})
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(True, json_response['is_completed'])
    
    def test_user_not_authorized(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        response = self.client.get("/api/list-task/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)