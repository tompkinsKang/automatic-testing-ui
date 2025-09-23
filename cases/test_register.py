from pages.register_page import RegisterPage
from playwright.sync_api import expect
import pytest
import uuid

class TestRegister:
    """注册功能"""

    # 登录用例执行前置后置，每个用例执行前都会自动执行
    @pytest.fixture(autouse=True,scope="function")
    def start_register_case(self,page):
        print("注册用例前置，打开新的注册页面")
        self.register = RegisterPage(page)
        self.register.navigate() # 打开注册页面
        yield
        print("后置")

    def test_register_1(self):
        """测试用户名为空，点注册"""
        self.register.fillRegister("", "123456")
        self.register.click_register_btn()
        expect(self.register.locator_usernameTips1).to_be_visible()
        expect(self.register.locator_usernameTips1).to_have_text("不能为空")

    def test_register_2(self):
        """测试用户名大于30字符"""
        self.register.fillRegister("a"*31, "123456")
        expect(self.register.locator_usernameTips2).to_be_visible()
        expect(self.register.locator_usernameTips2).to_have_text("用户名称1-30位字符")
        expect(self.register.locator_registerBtn).to_be_disabled() # 断言无法点击注册按钮

    def test_register_3(self):
        """测试用户名包含特殊字符"""
        self.register.fillRegister(" @!#%^&*()_+", "123456")
        expect(self.register.locator_usernameTips3).to_be_visible()
        expect(self.register.locator_usernameTips3).to_have_text("用户名称不能有特殊字符,请用中英文数字_")
        expect(self.register.locator_registerBtn).to_be_disabled()  # 断言无法点击注册按钮

    # pytest参数化会根据传入的参数，以及参数个数，生成多个用例。
    # pytest.mark.parametrize(参数名，参数值列表) ，参数值列表为二维列表，列表或者元组 [] or ()，其中每个元素都是要传入的参数
    @pytest.mark.parametrize("username,password",[["py","123456"]])
    def test_register_error(self,username,password):
        """测试注册失败，用户名已存在"""
        self.register.fillRegister(username,password)
        self.register.click_register_btn()
        expect(self.register.locator_registerError).to_be_visible()
        expect(self.register.locator_registerError).to_have_text("用户名已存在或不合法！")

    def test_register_success(self):
        """测试注册成功"""
        self.register.fillRegister(str(uuid.uuid4())[:7],str(uuid.uuid4())[:7])
        print("\n断言重定向")
        with self.register.page.expect_navigation(url="**/index.html"):
            self.register.click_register_btn()
        print("\n断言url和title")
        expect(self.register.page).to_have_url("/index.html")
        expect(self.register.page).to_have_title("首页")

        # # 3、Ajax方式，断言返回状态码和返回值
        # with self.register.page.expect_response("/api/register") as res:
        #     self.register.click_register_btn()
        # assert res.value.status == 200
        # assert res.value.ok


    def test_register_6(self):
        """测试密码为空且长度不符合要求"""
        self.register.fillRegister("py"," ")
        expect(self.register.locator_passwordTips1).to_be_visible()
        expect(self.register.locator_passwordTips1).to_have_text("不能为空")
        expect(self.register.locator_passwordTips2).to_be_visible()
        expect(self.register.locator_passwordTips2).to_have_text("密码6-16位字符")
        expect(self.register.locator_registerBtn).to_be_disabled()

    def test_register_6_1(self):
        """测试密码为空格"""
        self.register.fillRegister("py","      ")
        expect(self.register.locator_passwordTips1).to_be_visible()
        expect(self.register.locator_passwordTips1).to_have_text("不能为空")
        expect(self.register.locator_registerBtn).to_be_disabled()

    @pytest.mark.parametrize("password",[
        "5","17","0","a"*32
    ])
    def test_register_7(self,password):
        """测试密码长度不符合要求"""
        self.register.fillRegister("py",password)
        expect(self.register.locator_passwordTips2).to_be_visible()
        expect(self.register.locator_passwordTips2).to_have_text("密码6-16位字符")
        expect(self.register.locator_registerBtn).to_be_disabled()

    def test_register_8(self):
        """测试密码包含特殊字符"""
        self.register.fillRegister("py","!@#$%^&*")
        expect(self.register.locator_passwordTips3).to_be_visible()
        expect(self.register.locator_passwordTips3).to_have_text("不能有特殊字符,请用中英文数字下划线")
        expect(self.register.locator_registerBtn).to_be_disabled()


