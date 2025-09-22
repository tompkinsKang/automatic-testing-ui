from playwright.sync_api import Page

class AddProjectPage:
    def __init__(self,page:Page):
        self.page = page

        # 页面元素
        self.locator_project_name = page.get_by_label("项目名称:")
        self.locator_publish_app = page.get_by_label("所属应用:")
        self.locator_project_desc = page.get_by_label("项目描述:")
        self.locator_submitBtn = page.locator("#save_project")

        # 项目名称错误情况
        self.locator_projectNameTips1 = page.locator('[data-fv-validator="notEmpty"][data-fv-for="project_name"]')
        self.locator_projectNameTips2 = page.locator('[data-fv-validator="stringLength"][data-fv-for="project_name"]')
        self.locator_projectNameTips3 = page.locator('[data-fv-validator="regexp"][data-fv-for="project_name"]')

        # 所属应用错误情况
        self.locator_publishAppTips1 = page.locator("[data-fv-validator='stringLength'][data-fv-for='publish_app']")
        self.locator_publishAppTips2 = page.locator("[data-fv-validator='regexp'][data-fv-for='publish_app']")

        # 项目描述错误情况
        self.locator_projectDescTips1 = page.locator("[data-fv-validator='stringLength'][data-fv-for='project_desc']")

    # 添加项目页导航
    def navigate(self):
        self.page.goto("/add_project.html")

    # 输入项目名称
    def fillProjectName(self,project_name):
        self.locator_project_name.fill(project_name)

    # 输入所属应用
    def fillPublishApp(self,publish_app):
        self.locator_publish_app.fill(publish_app)

    # 输入项目描述
    def fillProjectDesc(self,project_desc):
        self.locator_project_desc.fill(project_desc)

    # 保存按钮
    def saveButton(self):
        self.locator_submitBtn.click()

    # 填写添加项目信息
    def fillAddProjcet(self,project_name,publish_app,project_desc):
        self.fillProjectName(project_name)
        self.fillPublishApp(publish_app)
        self.fillProjectDesc(project_desc)