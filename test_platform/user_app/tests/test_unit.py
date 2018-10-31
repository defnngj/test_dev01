from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class UserTestCase(TestCase):

    def setUp(self):
        User.objects.create_user("test01", "test01@mail.com", "test123456")

    def test_user_create(self):
        """测试创建用户"""
        User.objects.create_user("test02", "test02@mail.com", "test654321")
        user = User.objects.get(username="test02")
        self.assertEqual(user.email, "test02@mail.com")

    def test_user_select(self):
        """测试查询用户"""
        user = User.objects.get(username="test01")
        self.assertEqual(user.email, "test01@mail.com")

    def test_user_update(self):
        """测试更新用户"""
        user = User.objects.get(username="test01")
        user.username = "test02"
        user.email = "test02@mail.com"
        user.save()

# 运行测试的时候，不会真的调用数据库里面的数据

class IndexPageTest(TestCase):
    """测试index登录首页"""

    def test_index_page_renders_index_template(self):
        """断言是否用给定的index.html模版响应"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginActionTest(TestCase):

    def setUp(self):
        # Every test needs a client.
        User.objects.create_user("test01", "test01@mail.com", "test123456")
        self.client = Client()

    def test_login_null(self):
        """用户名密码为空"""
        # Issue a GET request.
        login_data= {"username":"", "password":""}
        response = self.client.post('/login_action/', data=login_data)
        login_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("用户名或者密码为空", login_html)

    def test_login_error(self):
        """用户名密码错误"""
        # Issue a GET request.
        login_data= {"username":"error", "password":"error"}
        response = self.client.post('/login_action/', data=login_data)
        login_html = response.content.decode("utf-8")
        self.assertEqual(response.status_code, 200)
        self.assertIn("用户名或者密码错误", login_html)

    def test_login_success(self):
        """登录成功"""
        login_data= {"username":"test01", "password":"test123456"}
        response = self.client.post('/login_action/', data=login_data)
        self.assertEqual(response.status_code, 302)


class LogoutTest(TestCase):
    """ 测试退出"""

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    def test_add_author_email(self):
        ''' 测试添加用户 '''
        user = User.objects.get(username="admin")
        self.assertEqual(user.username, "admin")
        self.assertEqual(user.email, "admin@mail.com")

    def test_login_action_username_password_null(self):
        ''' 用户名密码为空 '''
        response = self.client.post(
            '/login_action/', {'username': '', 'password': ''})
        login_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("用户名或者密码为空", login_html)

    def test_login_action_username_password_error(self):
        ''' 用户名密码错误 '''
        response = self.client.post(
            '/login_action/', {'username': 'abc', 'password': '123'})
        login_html = response.content.decode('utf-8')
        self.assertEqual(response.status_code, 200)
        self.assertIn("用户名或者密码错", login_html)

    def test_login_action_success(self):
        ''' 登录成功 '''
        user = {'username': 'admin', 'password': 'admin123456'}
        response = self.client.post('/login_action/', data=user)
        self.assertEqual(response.status_code, 302)


