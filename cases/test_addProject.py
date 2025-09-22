import pytest
from playwright.sync_api import expect
from pages.addProject_page import AddProjectPage

class TestAddProject:
    @pytest.fixture(autouse=True,scope="function")
    # 添加项目用例前置与后置
    def start_addproject_cases(self,page,login_save):
        print("添加项目的function前置，传入Login_save自动登录参数")
        self.add_project = AddProjectPage(page)
        self.add_project.navigate()
        yield
        print("后置")

    # 异常场景1：项目名称为空、项目名称超长、项目名称特殊符号
    @pytest.mark.parametrize("project_name",[
        "",
        "a"*31,
        "!@#$%^&*()+<>?:"
    ])
    def test_addproject_1(self,project_name):
        self.add_project.fillAddProjcet(project_name,"所属应用名称TEST","项目描述TEST")
        self.add_project.locator_submitBtn.click()
        expect(self.add_project.locator_projectNameTips1).to_be_visible()
        expect(self.add_project.locator_projectNameTips1).to_have_text("不能为空")
        expect(self.add_project.locator_submitBtn).to_be_disabled()

    # 异常场景2：所属应用名称超长、所属应用名称特殊符号
    # 异常场景3：项目描述超长
