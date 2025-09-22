from playwright.sync_api import Page

class RegisterPage:
    def __init__(self,page:Page):
        self.page = page

        # 页面元素
        self.locator_username = page.get_by_label("用 户 名:")
        self.locator_password = page.get_by_label("密     码:")
        self.locator_registerBtn = page.get_by_text("立即注册",exact=False)
        self.locator_loginBtn = page.get_by_text("已有账号？点这登录")

        # 用户名错误提示
        self.locator_usernameTips1 = page.locator('[data-fv-validator="notEmpty"][data-fv-for="username"]')
        self.locator_usernameTips2 = page.locator('[data-fv-validator="stringLength"][data-fv-for="username"]')
        self.locator_usernameTips3 = page.locator('[data-fv-validator="regexp"][data-fv-for="username"]')

        # 密码错误提示
        self.locator_passwordTips1 = page.locator('[data-fv-validator="notEmpty"][data-fv-for="password"]')
        self.locator_passwordTips2 = page.locator('[data-fv-validator="stringLength"][data-fv-for="password"]')
        self.locator_passwordTips3 = page.locator('[data-fv-validator="regexp"][data-fv-for="password"]')

        # 用户名或密码错误提示
        self.locator_registerError = page.get_by_text("用户名已存在或不合法！")

    # 注册页导航
    def navigate(self):
        self.page.goto("http://47.116.12.183/register.html")

    # 输入用户名
    def fill_username(self,username):
        self.locator_username.fill(username)

    # 输入密码
    def fill_password(self,password):
        self.locator_password.fill(password)

    # 点击已有账号，登录按钮
    def click_login_btn(self):
        self.locator_loginBtn.click()

    # 点击注册按钮
    def click_register_btn(self):
        self.locator_registerBtn.click()

    # 注册填写操作
    def fillRegister(self,username,password) -> None:
        self.fill_username(username)
        self.fill_password(password)


