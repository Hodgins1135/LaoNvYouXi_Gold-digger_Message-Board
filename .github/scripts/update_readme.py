from github import Github
import os
import re
from collections import defaultdict

def main():
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # 获取所有开放状态的 issue（排除 PR）
    open_issues = [issue for issue in repo.get_issues(state='open') if not issue.pull_request]
    
    # 按标签分类 issue
    categorized_issues = defaultdict(list)
    
    # 首先收集所有标签
    all_labels = set()
    for issue in open_issues:
        for label in issue.labels:
            all_labels.add(label.name)
        # 为无标签的 issue 添加特殊分类
        if not issue.labels:
            categorized_issues["无标签"].append(issue)
    
    # 按标签分组 issue
    for label_name in all_labels:
        for issue in open_issues:
            if any(l.name == label_name for l in issue.labels):
                categorized_issues[label_name].append(issue)
    
    # 按标签名称排序
    sorted_labels = sorted(categorized_issues.keys())
    
    # 生成分类的 Markdown 内容
    markdown_content = "## 最新\n\n"
    
    # 标签导航索引
    markdown_content += "### 标签导航\n"
    for label in sorted_labels:
        # 替换空格为连字符以创建有效的锚点
        anchor = label.replace(" ", "-")
        markdown_content += f"- [{label}](#{anchor}) ({len(categorized_issues[label])})\n"
    markdown_content += "\n"
    
    # 按标签显示 issue
    for label in sorted_labels:
        if label != "无标签" :
            # 创建锚点
            anchor = label.replace(" ", "-")
            markdown_content += f"### <a id='{anchor}'></a>{label} ({len(categorized_issues[label])})\n\n"
        
            # 添加问题列表
            for issue in categorized_issues[label]:
                created_at = issue.created_at.strftime("%Y-%m-%d")
                assignee = issue.assignee.login if issue.assignee else "未分配"
                markdown_content += f"- [{issue.title}]({issue.html_url}) "
                markdown_content += f"| 创建于: {created_at} | 负责人: {assignee}\n"
            
            markdown_content += "\n"
    
    # 读取当前 README
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()
    
    # 替换占位符区域
    pattern = r"<!-- ISSUE_LIST_START -->[\s\S]*?<!-- ISSUE_LIST_END -->"
    replacement = f"<!-- ISSUE_LIST_START -->\n{markdown_content}\n<!-- ISSUE_LIST_END -->"
    updated_readme = re.sub(pattern, replacement, readme_content)
    
    # 写入更新后的 README
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(updated_readme)

if __name__ == "__main__":
    main()
