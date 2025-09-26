import pytest
from pages.login_page import LoginPage
from pytest import Item
import allure

pytest_plugins = ['plugins.pytest_playwright']

# 账号py的保存登录
@pytest.fixture(scope="session")
def py_save(browser,base_url,pytestconfig):
    print("登录py，并且保存cookies")
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    LoginPage(page).navigate()
    LoginPage(page).fillLogin("py", "123456")
    LoginPage(page).click_login_btn()
    # 等待登录成功后重定向
    page.wait_for_url(url="**/index.html")
    storage_path = pytestconfig.rootpath.joinpath("auth/state.json")
    context.storage_state(path=str(storage_path))
    context.close()

# 账号admin的保存登录
@pytest.fixture(scope="session")
def admin_save(browser,base_url,pytestconfig):
    print("登录admin，并且保存cookies")
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    LoginPage(page).navigate()
    LoginPage(page).fillLogin("admin", "123456")
    LoginPage(page).click_login_btn()
    # 等待登录成功后重定向
    page.wait_for_url(url="**/index.html")
    storage_path = pytestconfig.rootpath.joinpath("auth/admin.json")
    context.storage_state(path=str(storage_path))
    context.close()

# 重写默认的browser_context_args，加载账号py的cookies
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright, pytestconfig):
 """
添加context 上下文参数，默认每个页面加载cookies
 :param browser_context_args:
 :param playwright:
 :return:
 """
 return {
 "storage_state":pytestconfig.rootpath.joinpath("auth/state.json"),
 **browser_context_args,
 }

# admin的context，传入admin_save依赖保证admin.json存在
@pytest.fixture(scope="module")
def admin_context(browser,base_url,pytestconfig,admin_save):
    context = browser.new_context(
        base_url=base_url,
        storage_state=pytestconfig.rootpath.joinpath("auth/admin.json")
    )
    yield context
    context.close()

def pytest_runtest_call(item: Item):
    # 动态添加测试类的allure.feature()
    if item.parent._obj.__doc__:
        allure.dynamic.feature(item.parent._obj.__doc__)
    # 动态添加测试用例的title标题allure.title()
    if item.function.__doc__:
        allure.dynamic.title(item.function.__doc__)