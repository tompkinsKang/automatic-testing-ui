import uuid
import pytest
from playwright.sync_api import expect
from pages.addProject_page import AddProjectPage
from pages.projectlist_page import ProjectList

class TestAdmin:
    """多账号测试"""

    # 测试多账号的前置后置操作
    @pytest.fixture(autouse=True)
    def start(self,page,py_save,admin_context):
        # 用户py
        self.user_py = AddProjectPage(page)
        self.user_py.navigate()
        # 用户admin
        page2 = admin_context.new_page()
        self.user_admin = ProjectList(page2)
        self.user_admin.navigate()
        yield
        print("后置")
        page2.close() # py是内置的，自动关闭，admin是自己创建的，需要手动关闭

    def test_delete_project(self):
        """测试py账号创建，admin账号删除项目"""
        # 账号1py添加项目
        new_project_name = str(uuid.uuid4())[:8]
        self.user_py.fillAddProject(new_project_name, "test", "test")
        self.user_py.locator_submitBtn.click()
        # 断言添加项目成功
        expect(self.user_py.page).to_have_title("项目列表")
        expect(self.user_py.page).to_have_url("/list_project.html")
        expect(self.user_py.page.locator("//*[@id='table']/tbody/tr[1]/td[3]/a")).to_have_text(new_project_name)

        # 账号2admin删除项目
        self.user_admin.search(new_project_name)
        self.user_admin.delete()

        # 再次查询该项目，未找到则成功
        self.user_admin.search(new_project_name)
        expect(self.user_admin.locator_search_fail_info).to_be_visible()
        expect(self.user_admin.locator_projectname).not_to_be_visible()




