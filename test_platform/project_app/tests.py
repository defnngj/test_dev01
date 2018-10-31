from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from project_app.models import Project


# Create your tests here.
class ProjectTest(TestCase):
    """ 项目管理 """

    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test123456")
        Project.objects.create(name="测试平台项目", describe="描述")
        self.client = Client()
        login_data = {"username": "test01", "password": "test123456"}
        self.client.post('/login_action/', data=login_data)

    def test_project_manage(self):
        """项目管理"""
        response = self.client.get('/manage/project_manage/')
        project_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("退出", project_html)
        self.assertIn("测试平台项目", project_html)


class ProjectAddTest(TestCase):
    ''' 添加项目 '''

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')
        Project.objects.create(name="xx项目", describe="xx描述")
        login_user = {'username': 'admin', 'password': 'admin123456'}
        self.client.post('/login_action/', data=login_user)  # 预先登录

    def test_project_add_test(self):
        ''' 添加成功，做302跳转 '''
        data = {"name": "test111", "describe": "test111", "status": True}
        response = self.client.post('/manage/add_project/', data=data)
        project_html = response.content.decode('utf-8')
        print(project_html)
        self.assertEqual(response.status_code, 302)
        

# 测试编辑接口的话，需要先创建一条已经存在的数据，再对该数据进行提交，注意ID一致，否则就是创建了。

        

