import pytest
from pages.login_page import LoginPage

#全局登录并且保存Cookies
@pytest.fixture(scope="session")
def login_save(browser,pytestconfig):
    print("全局登录，并且保存cookies")
    context = browser.new_context(base_url="http://47.116.12.183")
    page = context.new_page()
    LoginPage(page).navigate()
    LoginPage(page).fillLogin("py", "123456")
    LoginPage(page).click_login_btn()
    # 等待登录成功后重定向
    page.wait_for_url(url="**/index.html")
    # 保存storage state 到文件
    storage_path = pytestconfig.rootpath.joinpath("auth/state.json")
    context.storage_state(path=storage_path)
    context.close()

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
