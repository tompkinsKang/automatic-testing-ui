import uuid
import pytest
from playwright.sync_api import expect
from mocks.mock_api import mock_project_400,mock_project_500
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

    # 异常场景1：项目名称为空
    def test_addproject_1(self):
        self.add_project.fillAddProject("","所属应用名称TEST","项目描述TEST")
        self.add_project.locator_submitBtn.click()
        expect(self.add_project.locator_projectNameTips1).to_be_visible()
        expect(self.add_project.locator_projectNameTips1).to_have_text("不能为空")
        expect(self.add_project.locator_submitBtn).to_be_disabled()

    # 异常场景2：项目名称1-30
    def test_addproject_2(self):
        self.add_project.fillAddProject("a"*31,"所属应用名称TEST","项目描述TEST")
        expect(self.add_project.locator_projectNameTips2).to_be_visible()
        expect(self.add_project.locator_projectNameTips2).to_have_text("项目名称1-30位字符")
        expect(self.add_project.locator_submitBtn).to_be_disabled()

    # 异常场景3：项目名称包含特殊字符
    def test_addproject_3(self):
        self.add_project.fillAddProject("!@#$%^&*()+<>?:","所属应用名称TEST","项目描述TEST")
        expect(self.add_project.locator_projectNameTips3).to_be_visible()
        expect(self.add_project.locator_projectNameTips3).to_have_text("项目名称不能有特殊字符,请用中英文数字_")
        expect(self.add_project.locator_submitBtn).to_be_disabled()

    # 异常场景4：所属应用超长 最大30
    def test_addproject_4(self):
        self.add_project.fillAddProject("项目名称TEST","a*"*31,"项目描述TEST")
        expect(self.add_project.locator_publishAppTips1).to_be_visible()
        expect(self.add_project.locator_publishAppTips1).to_have_text("最大30位字符")
        expect(self.add_project.locator_submitBtn).to_be_disabled()

    # 异常场景5：所属应用特殊字符
    def test_addproject_5(self):
        self.add_project.fillAddProject("项目名称TEST","!@#$%^&*()+<>?:","项目描述TEST")
        expect(self.add_project.locator_publishAppTips2).to_be_visible()
        expect(self.add_project.locator_publishAppTips2).to_have_text("不能有特殊字符")
        expect(self.add_project.locator_submitBtn).to_be_disabled()

    # 异常场景6：项目描述超长 最大200
    def test_addproject_6(self):
        self.add_project.fillAddProject("项目名称TEST","所属应用名称TEST","a"*201)
        expect(self.add_project.locator_projectDescTips1).to_be_visible()
        expect(self.add_project.locator_projectDescTips1).to_have_text("最大200位字符")
        expect(self.add_project.locator_submitBtn).to_be_disabled()

    # 正常场景, 添加项目成功,Ajax请求断言，url、title断言，断言新添加项目在列表中显示
    def test_addproject_success(self):
        new_project_name = str(uuid.uuid4())[:8]
        self.add_project.fillAddProject(new_project_name,"test","test")
        with self.add_project.page.expect_response("/api/project") as res:
            self.add_project.locator_submitBtn.click()
        assert res.value.status == 201
        assert res.value.ok
        expect(self.add_project.page).to_have_title("项目列表")
        expect(self.add_project.page).to_have_url("/list_project.html")
        # 断言项目列表中，table的第一行第三列是新添加的项目名称
        expect(self.add_project.page.locator("//*[@id='table']/tbody/tr[1]/td[3]")).to_have_text(new_project_name)

    def test_add_project_400(self,page):
        self.add_project.fillAddProject("yoyo","a","a")
        page.route(**mock_project_400) # 返回400响应
        self.add_project.locator_submitBtn.click()
        expect(self.add_project.page.locator(".bootbox-body")).to_be_visible()
        expect(self.add_project.page.locator(".bootbox-body")).to_contain_text("已存在")

    def test_add_project_500(self,page):
        self.add_project.fillAddProject("yoyo","a","a")
        page.route(**mock_project_500) # 返回500响应
        self.add_project.locator_submitBtn.click()
        expect(self.add_project.page.locator(".bootbox-body")).to_be_visible()
        expect(self.add_project.page.locator(".bootbox-body")).to_contain_text("操作异常")
