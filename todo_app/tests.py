from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Task
from django.urls import reverse

class TaskViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.admin = User.objects.create_superuser(username='admin', password='admin123')
        self.task = Task.objects.create(user=self.user, title='Test Task')

    def test_login_required(self):
        response = self.client.get(reverse('task_list'))
        self.assertRedirects(response, '/login/?next=/')

    def test_user_task_list(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, 'Test Task')

    def test_admin_can_see_all_tasks(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.get(reverse('task_list'))
        self.assertContains(response, 'Test Task')

    def test_add_task(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('add_task'), {'title': 'New Task'})
        self.assertEqual(Task.objects.count(), 2)

    def test_delete_task(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(Task.objects.count(), 0)

