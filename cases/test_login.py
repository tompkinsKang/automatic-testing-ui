from pages.login_page import LoginPage
from playwright.sync_api import expect
import pytest

class TestLogin:

    # 登录用例执行前置后置
    @pytest.fixture(autouse=True,scope="function")
    def start_login_case(self,page):
        print("登陆用例的前置，打开新的登录页")
        self.login = LoginPage(page)
        self.login.navigate()
        yield
        print("后置")

    # 用例1，用户名为空，点登录
    def test_login_1(self):
        self.login.fillLogin("", "123456")
        self.login.click_login_btn()
        expect(self.login.locator_usernameTips1).to_be_visible()
        expect(self.login.locator_usernameTips1).to_have_text("不能为空")

    # 用例2，用户名大于30字符
    def test_login_2(self):
        self.login.fillLogin("a"*31, "123456")
        expect(self.login.locator_usernameTips2).to_be_visible()
        expect(self.login.locator_usernameTips2).to_have_text("用户名称1-30位字符")
        expect(self.login.locator_loginBtn).to_be_disabled() # 登录按钮不可点击

    # 用例3，用户名包含特殊字符
    def test_login_3(self):
        self.login.fillLogin(" @!#%^&*()_+", "123456")
        expect(self.login.locator_usernameTips3).to_be_visible()
        expect(self.login.locator_usernameTips3).to_have_text("用户名称不能有特殊字符,请用中英文数字_")
        expect(self.login.locator_loginBtn).to_be_disabled()  # 登录按钮不可点击

    # 用例4，登陆失败，
    # pytest参数化会根据传入的参数，以及参数个数，生成多个用例。
    # pytest.mark.parametrize(参数名，参数值列表) ，参数值列表为二维列表，列表或者元组 [] or ()，其中每个元素都是要传入的参数
    @pytest.mark.parametrize("username,password",[
                             ["12345678","123456"],
                             ["sadasdasd","asdasd"]])
    def test_login_error(self,username,password):
        self.login.fillLogin(username,password)
        self.login.click_login_btn()
        expect(self.login.locator_loginError).to_be_visible()
        expect(self.login.locator_loginError).to_have_text("账号或密码不正确！")

    # 用例5，登陆成功
    def test_login_success(self):
        self.login.fillLogin("llh","admin123")

        # self.login.click_login_btn()

        # # 2、断言监听重定向是否正确
        # with self.login.page.expect_navigation(url="**/index.html"):
        #     self.login.click_login_btn()
        #
        # # 1、判断url和title
        # expect(self.login.page).to_have_url("http://47.116.12.183/index.html")
        # expect(self.login.page).to_have_title("首页")

        # 3、Ajax方式，断言返回状态码和返回值
        with self.login.page.expect_response("http://47.116.12.183/api/login") as res:
            self.login.click_login_btn()
        assert res.value.status == 200
        assert res.value.ok

    def test_login_6(self):
        self.login.fillLogin("llh","      ")
        expect(self.login.locator_passwordTips1).to_be_visible()
        expect(self.login.locator_passwordTips1).to_have_text("不能为空")
        expect(self.login.locator_loginBtn).to_be_disabled()

    @pytest.mark.parametrize("password",[
        "5","17","0","a"*32
    ])
    def test_login_7(self,password):
        self.login.fillLogin("llh",password)
        expect(self.login.locator_passwordTips2).to_be_visible()
        expect(self.login.locator_passwordTips2).to_have_text("密码6-16位字符")
        expect(self.login.locator_loginBtn).to_be_disabled()

    def test_login_8(self):
        self.login.fillLogin("llh","!@#$%^&*")
        expect(self.login.locator_passwordTips3).to_be_visible()
        expect(self.login.locator_passwordTips3).to_have_text("不能有特殊字符,请用中英文数字下划线")
        expect(self.login.locator_loginBtn).to_be_disabled()

    def test_login_register(self):
        with self.login.page.expect_navigation(url="**/register.html"):
            self.login.click_register_btn()
        #     expect(self.login.locator_register_btn).to_have_attribute("href","register.html")
        expect(self.login.page).to_have_title("注册")
        expect(self.login.page).to_have_url("http://47.116.12.183/register.html")

