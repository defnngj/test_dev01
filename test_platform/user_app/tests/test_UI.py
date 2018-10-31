from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver import Chrome
from time import sleep
from django.contrib.auth.models import User
from project_app.models import Project


class LoginTests(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        """初始化数据"""
        User.objects.create_user("test01", "test01@mail.com", "test123456")
        Project.objects.create(name="测试平台项目", describe="描述")

    def test_login(self):
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys("")
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys("")
        sleep(1)
        self.driver.find_element_by_id('LoginButton').click()
        error_hint = self.driver.find_element_by_id("error").text
        print(error_hint)
        self.assertEqual("用户名或者密码为空", error_hint)

    def test_login_error(self):
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys("error")
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys("error")
        sleep(1)
        self.driver.find_element_by_id('LoginButton').click()
        error_hint = self.driver.find_element_by_id("error").text
        print(error_hint)
        self.assertEqual("用户名或者密码错误", error_hint)

    def test_login_success(self):
        self.driver.get('%s%s' % (self.live_server_url, '/'))
        username_input = self.driver.find_element_by_name("username")
        username_input.send_keys("test01")
        password_input = self.driver.find_element_by_name("password")
        password_input.send_keys("test123456")
        sleep(1)
        self.driver.find_element_by_id('LoginButton').click()
        error_hint = self.driver.find_element_by_class_name("navbar-brand").text
        print(error_hint)
        self.assertEqual("测试平台", error_hint)

