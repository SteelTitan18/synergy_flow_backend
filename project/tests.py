from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

from project.models import CustomUser, Project, Task

# Create your tests here.
class ProjectViewSetTests(APITestCase):
    def setUp(self):
        # Création de l'utilisateur admin et du membre
        self.admin_user = CustomUser.objects.create_superuser(username='admin', password='adminpass', user_type= 'ADM')
        self.member_user = CustomUser.objects.create_user(username='member', password='memberpass', user_type= 'MBR')

        # Création d'un projet
        self.project = Project.objects.create(label='Test Project', description='This is a test project')

        # Obtenir des tokens pour les utilisateurs
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.member_token = str(RefreshToken.for_user(self.member_user).access_token)

        # URL des projets
        self.list_url = reverse('project-list')
        self.detail_url = reverse('project-detail', args=[self.project.pk])

    
    def test_admin_can_list_projects(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', [])), 1)

    def test_member_can_list_projects(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results', [])), 1)

    def test_admin_can_create_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        data = {'label':'Test Project', 'description':'This is a test project'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_member_cannot_create_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        data = {'label':'Test Project', 'description':'This is a test project'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_retrieve_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], 'Test Project')

    def test_member_can_retrieve_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], 'Test Project')

    def test_admin_can_update_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        data = {'label':'Test Project update', 'description':'This is a test project'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.label, 'Test Project update')

    def test_member_cannot_update_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        data = {'label':'Test Project update', 'description':'This is a test project'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

    def test_member_cannot_delete_project(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TaskViewSetTests(APITestCase):

    def setUp(self):
        # Création des utilisateurs admin et membre
        self.admin_user = CustomUser.objects.create_superuser(username='admin', password='adminpass', user_type= 'ADM')
        self.member_user = CustomUser.objects.create_user(username='member', password='memberpass', user_type= 'MBR')

        # Création d'un autre utilisateur pour assigner la tâche
        self.assignee_user = CustomUser.objects.create_user(username='assignee', password='assigneepass', user_type= 'MBR')

        # Création d'un projet
        self.project = Project.objects.create(label='Test Project', description='Ceci est un test')

        # Création d'une tâche
        self.task = Task.objects.create(
            task_author=self.admin_user,
            task_project=self.project,
            label='Test Task',
            start_date='2024-01-01',
            end_date='2024-01-02'
        )
        self.task.task_assignees.add(self.assignee_user)

        # Obtenir des tokens pour les utilisateurs
        self.admin_token = str(RefreshToken.for_user(self.admin_user).access_token)
        self.member_token = str(RefreshToken.for_user(self.member_user).access_token)
        self.assignee_token = str(RefreshToken.for_user(self.assignee_user).access_token)

        # URLs des tâches
        self.list_url = reverse('task-list')
        self.detail_url = reverse('task-detail', args=[self.task.pk])

    def test_admin_can_list_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        results = data.get('results', [])
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]['label'], 'Test Task')

    def test_member_can_list_tasks(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        results = data.get('results', [])
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]['label'], 'Test Task')

    def test_admin_can_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        data = {
            'task_author': self.admin_user.id,
            'task_project': self.project.id,
            'task_assignees': [self.assignee_user.id],
            'label': 'New Task',
            'start_date': '2024-02-01',
            'end_date': '2024-02-02',
            'task_priority': 'MDM',
            'task_status': 'PRG'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_member_cannot_create_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        data = {
            'task_author': self.admin_user.id,
            'task_project': self.project.id,
            'task_assignees': [self.assignee_user.id],
            'label': 'New Task',
            'start_date': '2024-02-01',
            'end_date': '2024-02-02',
            'task_priority': 'MDM',
            'task_status': 'PRG'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_retrieve_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], 'Test Task')

    def test_assignee_can_retrieve_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.assignee_token)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['label'], 'Test Task')

    def test_admin_can_update_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        data = {
            'task_author': self.admin_user.id,
            'task_project': self.project.id,
            'task_assignees': [self.assignee_user.id],
            'label': 'Updated Task',
            'start_date': '2024-02-01',
            'end_date': '2024-02-02',
            'task_priority': 'MDM',
            'task_status': 'PRG'
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.label, 'Updated Task')

    def test_assignee_can_update_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.assignee_token)
        data = {
            'task_author': self.admin_user.id,
            'task_project': self.project.id,
            'task_assignees': [self.assignee_user.id],
            'label': 'Updated Task',
            'start_date': '2024-02-01',
            'end_date': '2024-02-02',
            'task_priority': 'MDM',
            'task_status': 'PRG'
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.label, 'Updated Task')

    def test_member_cannot_update_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        data = {'label': 'Updated Task'}
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_member_cannot_delete_task(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.member_token)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SigninViewTests(APITestCase):

    def setUp(self):
        # Créer un utilisateur pour les tests
        self.username = 'testuser'
        self.email = 'testuser@example.com'
        self.password = 'testpassword'
        self.user = CustomUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )
        self.url = '/api/project/login/'  # URL mise à jour pour la vue de connexion

    def test_login_with_username_success(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['email'], self.email)

    def test_login_with_email_success(self):
        data = {
            'username': self.email,
            'password': self.password
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['username'], self.username)
        self.assertEqual(response.data['email'], self.email)

    def test_login_with_incorrect_password(self):
        data = {
            'username': self.username,
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'error': 'Incorrect password'})

    def test_login_with_non_existent_user(self):
        data = {
            'username': 'nonexistentuser',
            'password': self.password
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'User not found'})