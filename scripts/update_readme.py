from github import Github
import os
import re

def main():
    # 获取环境变量
    token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('GITHUB_REPOSITORY')
    
    # 初始化GitHub API
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    # 获取所有开放的issue
    open_issues = repo.get_issues(state='open')
    
    # 生成Markdown格式的issue列表
    issue_list = "## 最新问题反馈\n\n"
    issue_list += "| 标题 | 标签 | 创建时间 |\n"
    issue_list += "|------|------|----------|\n"
    
    for issue in open_issues:
        # 跳过Pull Request（GitHub API将PR视为issue）
        if issue.pull_request:
            continue
            
        # 获取标签
        labels = ", ".join([label.name for label in issue.labels])
        created_at = issue.created_at.strftime("%Y-%m-%d")
        
        issue_list += f"| [{issue.title}]({issue.html_url}) | {labels} | {created_at} |\n"
    
    # 读取当前README内容
    with open("README.md", "r", encoding="utf-8") as file:
        readme_content = file.read()
    
    # 使用正则表达式替换占位符区域
    pattern = r"<!-- ISSUE_LIST_START -->[\s\S]*?<!-- ISSUE_LIST_END -->"
    replacement = f"<!-- ISSUE_LIST_START -->\n{issue_list}\n<!-- ISSUE_LIST_END -->"
    
    updated_readme = re.sub(pattern, replacement, readme_content)
    
    # 写入更新后的README
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(updated_readme)

if __name__ == "__main__":
    main()
