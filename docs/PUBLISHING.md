# GitHub 发布

建议将 `search-rsi` 作为独立仓库，而非上传整个父级调研目录。父级包含第三方源码、论文、大型数据与探索记录。

## 当前状态

本地初始化 Git；尚未设置远程、创建 GitHub 仓库或推送。初始化时本机 gh 未登录，Git 提交身份未配置。是否公开与开源许可证由项目所有者决定。可先建私有仓库，正式实验与文档成熟后公开。

## 发布前

1. 检查 `git status --short`，确认仅提交代码、配置模板、文档与小型虚构 fixture。
2. 选择许可证；未来接入第三方实现时保留其许可和署名。
3. 配置提交身份并登录 `gh auth login`。凭证不要复制到项目文件或聊天中。
4. 确定 GitHub owner、仓库名称与可见性。

配置身份后，在项目根目录执行本地首个提交：

```bash
git add .
git diff --cached --stat
git diff --cached
git commit -m "Initialize search RSI research scaffold"
```

如果决定新建私有仓库（替换 OWNER）：

```bash
gh repo create OWNER/search-rsi --private --source=. --remote=origin --push
```

已有远程仓库时应先检查其历史，不能直接覆盖或强推。实际推送需要明确目标与可见性。

`runs/`、`data/`、`checkpoints/`、`third_party/`、`.env` 和虚拟环境已被忽略。正式结果可整理到单独的报告目录，筛除敏感原始内容后再提交；Git ignore 不会自动移除已经跟踪的文件。
