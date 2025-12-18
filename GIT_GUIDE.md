# Study-Tracker 项目 Git 使用指南

## 1. 项目介绍

Study-Tracker 是一个用于跟踪学习进度的全栈应用，包含前端和后端两部分。本指南将帮助开发者了解如何使用 Git 对该项目进行版本控制和协作开发。

## 2. Git 安装与配置

### 2.1 安装 Git

- **Windows**: 下载并安装 [Git for Windows](https://gitforwindows.org/)
- **macOS**: 使用 Homebrew 安装 `brew install git`
- **Linux**: 使用包管理器安装，如 Ubuntu `sudo apt install git`

### 2.2 配置 Git

```bash
# 配置用户名和邮箱
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 配置默认编辑器
git config --global core.editor "code --wait"  # 使用 VS Code

# 配置自动换行处理
git config --global core.autocrlf true  # Windows
git config --global core.autocrlf input  # macOS/Linux

# 显示颜色
git config --global color.ui true
```

## 3. 代码克隆与初始化

### 3.1 克隆远程仓库

```bash
# 克隆项目到本地
git clone <仓库地址>

# 进入项目目录
cd Study-Tracker
```

### 3.2 初始化本地仓库（如果是新项目）

```bash
# 初始化 Git 仓库
git init

# 添加远程仓库
git remote add origin <仓库地址>
```

## 4. 分支管理

### 4.1 分支命名规范

- **master/main**: 主分支，用于发布稳定版本
- **dev**: 开发分支，用于集成所有功能开发
- **feature/xxx**: 功能分支，用于开发新功能
- **bugfix/xxx**: 修复分支，用于修复 bug
- **hotfix/xxx**: 热修复分支，用于修复生产环境的紧急问题

### 4.2 分支操作

```bash
# 查看所有分支
git branch -a

# 创建新分支
git checkout -b feature/user-authentication

# 切换分支
git checkout dev

# 合并分支（将 feature 分支合并到当前分支）
git merge feature/user-authentication

# 删除本地分支
git branch -d feature/user-authentication

# 删除远程分支
git push origin --delete feature/user-authentication
```

## 5. 提交规范

### 5.1 提交信息格式

```
<类型>(<范围>): <描述>

[可选的详细描述]

[可选的引用]
```

### 5.2 提交类型

- **feat**: 新功能
- **fix**: 修复 bug
- **docs**: 文档更新
- **style**: 代码格式调整（不影响功能）
- **refactor**: 代码重构（不新增功能或修复 bug）
- **test**: 测试相关
- **chore**: 构建过程或辅助工具的变动
- **perf**: 性能优化

### 5.3 提交示例

```bash
git commit -m "feat(auth): 添加用户注册功能"
git commit -m "fix(api): 修复登录接口的密码验证问题"
git commit -m "docs(readme): 更新项目说明文档"
```

## 6. 开发流程

1. **创建分支**: 从 `dev` 分支创建新的功能分支
2. **开发代码**: 在功能分支上进行开发
3. **提交代码**: 定期提交代码，保持提交信息清晰
4. **推送分支**: 将本地分支推送到远程仓库
5. **创建 PR**: 功能开发完成后，创建 Pull Request 到 `dev` 分支
6. **代码审查**: 团队成员进行代码审查
7. **合并分支**: 代码审查通过后，将功能分支合并到 `dev` 分支
8. **删除分支**: 合并完成后，删除本地和远程的功能分支

### 6.1 开发流程示例

```bash
# 从 dev 分支创建功能分支
git checkout dev
git pull origin dev
git checkout -b feature/task-management

# 开发代码...

# 提交代码
git add .
git commit -m "feat(task): 添加任务创建功能"
git push origin feature/task-management

# 创建 PR（在 GitHub/GitLab 上操作）

# 代码审查通过后，合并分支
git checkout dev
git pull origin dev
git merge feature/task-management
git push origin dev

# 删除分支
git branch -d feature/task-management
git push origin --delete feature/task-management
```

## 7. 代码合并与冲突解决

### 7.1 合并冲突

当合并分支时，如果同一文件的同一部分被不同的分支修改，Git 会提示冲突。需要手动解决冲突后再提交。

### 7.2 解决冲突步骤

1. **查看冲突文件**: `git status`
2. **编辑冲突文件**: 手动修改包含冲突标记的文件
3. **标记冲突已解决**: `git add <冲突文件>`
4. **完成合并**: `git commit`

### 7.3 冲突文件示例

```python
<<<<<<< HEAD
# 当前分支的代码
def get_user_by_username(db, username):
    return db.query(User).filter(User.username == username).first()
=======
# 要合并分支的代码
def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()
>>>>>>> feature/async-db
```

## 8. 远程仓库操作

```bash
# 查看远程仓库
git remote -v

# 拉取远程仓库代码
git pull origin dev

# 推送本地分支到远程
git push origin feature/user-authentication

# 强制推送（谨慎使用）
git push origin feature/user-authentication --force

# 同步远程分支信息
git fetch origin
```

## 9. 常见问题与解决方案

### 9.1 忘记配置用户名和邮箱

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 9.2 提交错误的文件

```bash
# 撤销最后一次提交（保留修改）
git reset --soft HEAD~1

# 撤销最后一次提交（不保留修改）
git reset --hard HEAD~1
```

### 9.3 误删本地分支

```bash
# 查看最近的操作记录
git reflog

# 恢复删除的分支
git checkout -b feature/task-management <commit-hash>
```

### 9.4 本地代码与远程代码冲突

```bash
# 拉取远程代码并尝试自动合并
git pull origin dev --rebase

# 如果有冲突，解决后继续
git rebase --continue
```

## 10. 最佳实践

1. **定期拉取代码**: 每天开始工作前，先拉取最新的代码
2. **小步提交**: 每个提交只包含一个功能或一个 bug 修复
3. **清晰的提交信息**: 使用规范的提交信息格式，便于后续查阅和维护
4. **合理使用分支**: 每个功能或 bug 修复都应该在独立的分支上进行
5. **代码审查**: 所有代码变更都应该经过代码审查后再合并到主分支
6. **定期备份**: 确保代码定期推送到远程仓库，防止本地代码丢失

## 11. 参考资源

- [Git 官方文档](https://git-scm.com/doc)
- [Pro Git 电子书](https://git-scm.com/book/en/v2)
- [GitHub Git 指南](https://guides.github.com/introduction/git-handbook/)
- [Git 分支管理策略](https://nvie.com/posts/a-successful-git-branching-model/)

---

**注意**: 请严格遵循本指南的规范和流程，确保项目代码的质量和可维护性。如有任何问题，请随时向团队成员寻求帮助。