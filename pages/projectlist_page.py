from playwright.sync_api import Page
class ProjectList:

    def __init__(self,page:Page):
        self.page = page

        # 页面元素
        self.locator_projectname_search = self.page.get_by_placeholder("项目名称")
        self.locator_search_btn = self.page.get_by_text("搜索")
        self.locator_addproject_btn = self.page.locator("#btn_add")
        self.locator_projectname = self.page.locator("//*[@id='table']/tbody/tr[1]/td[3]/a")
        self.locator_update_btn = self.page.locator("//*[@id='table']/tbody/tr[1]/td[9]/a[1]")
        self.locator_delete_btn = self.page.locator("//*[@id='table']/tbody/tr[1]/td[9]/a[2]")
        # 查询失败
        self.locator_search_fail_info = self.page.get_by_text("没有找到匹配的记录")
        # 无权删除弹窗
        self.locator_delete_fail = self.page.get_by_text('操作异常："无权限操作，请联系管理员"')
        self.locator_delete_fail_btn = self.page.get_by_text('确定')
        # 删除弹窗
        self.locator_delete_success = self.page.get_by_text("确定要删除选中的数据？")
        self.locator_delete_success_cancel_btn = self.page.get_by_text("取消操作")
        self.locator_delete_success_confirm_btn = self.page.get_by_text("确定删除")




    # 项目列表页面导航
    def navigate(self):
        self.page.goto("/list_project.html")

    # 根据项目名称查询
    def search(self,project_name):
        self.locator_projectname_search.fill(project_name)
        self.locator_search_btn.click()

    def delete(self):
        self.locator_delete_btn.click()
        self.locator_delete_success_confirm_btn.click()





