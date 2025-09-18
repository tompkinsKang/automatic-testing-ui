import pytest
from playwright.sync_api import sync_playwright

# conftest 为 pytest 提供配置和环境的文件，可以在其中定义夹具（fixtures）来管理测试的前置和后置条件
@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()



