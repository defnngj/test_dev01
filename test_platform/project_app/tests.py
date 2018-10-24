from django.test import TestCase
from datetime import datetime
from project_app.models import Project
from django.contrib.auth.models import User


# Create your tests here.
class ProjectMangeTest(TestCase):
    ''' 项目管理 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Project.objects.create(name="xx项目", describe="xx描述")
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_project_manage_success(self):
        ''' 测试发布会:xiaomi5 '''
        response = self.client.post('/manage/project_manage/')
        project_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("xx项目", project_html)
        self.assertIn("xx描述", project_html)
