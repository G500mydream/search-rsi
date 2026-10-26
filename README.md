# Search RSI

研究交互经验能否让 Search Agent 在新的问题上搜索得更好，以及如何用有限验证预算选择值得保留的策略。

**状态：项目骨架与离线演示。尚未接入真实 LLM、BrowseComp-Plus、ACE 或 ReasoningBank；没有正式实验结果。** 当前 demo 是确定性检索和字段抽取，不是 ReAct，也不执行跨任务学习。这里的 RSI 指计划研究的外部策略持续改进，不代表已实现递归自我改进。

## 快速开始

需要 Python 3.11+。离线 demo 不需要安装第三方依赖、API key 或下载数据。在项目根目录运行：

```bash
bash scripts/run_demo.sh
PYTHONPATH=src python -m unittest discover -s tests -v
```

也可以安装为本地包（首次构建可能需要联网获取构建工具）：

```bash
python -m venv .venv
.venv/bin/python -m pip install -e .
.venv/bin/search-rsi --config configs/demo.toml
```

demo 使用人工编写的虚构文档，输出到 `runs/demo-*/`：

- `manifest.json`：配置、数据哈希、Python 与 Git 版本信息。
- `trajectories.jsonl`：搜索查询、结果、打开的文档、回答与引用。
- `metrics.jsonl`：逐题答案匹配、证据 ID 指标与工具调用数。
- `memory.json`：冻结的空记忆快照。
- `summary.json`：演示汇总；`cross_task_learning` 为 false。

演示成绩只验证程序链路，不是模型能力或学习收益。引用 ID 匹配不等于语义上的引用支持度。

## 代码结构

```text
configs/                  离线 demo 与明确标记 planned 的实验配置
examples/toy/             可提交的小型虚构 fixture
src/search_rsi/
  agent.py                有工具预算的离线执行循环
  environments/           环境适配；当前仅 toy
  models.py               确定性演示回答器；真实 API 待实现
  learners/               当前仅冻结记忆对照
  selection.py            策略接受机制的预留位置
  evaluation.py           与 Agent 分离的评分逻辑
  runner.py               演示运行和产物管理
  logging.py              JSON/JSONL 日志
scripts/                  可执行入口
tests/                    预算、标签边界与端到端检查
```

`fixed.toml`、`episodic.toml`、`ace.toml`、`reasoningbank.toml` 和 `verified.toml` 是研究配置模板，运行器会拒绝执行，避免把尚未实现的方法当作实验。

## 研究路线

1. 固定 BrowseComp-Plus 上游版本，复现单题检索和评分。
2. 接入真实模型与固定 ReAct 搜索 baseline，补全 usage 和费用记录。
3. 建立任务流、独立验证集和冻结测试集，完成失败归因 pilot。
4. 依次接入案例记忆、ACE 与 ReasoningBank，记录与原方法的适配差异。
5. 比较直接接受与验证后接受策略；计入反思和验证成本。

优先保持执行器、检索器和工具预算可比，避免把检索工具升级或更多计算误当作学习收益。

详见 [架构](docs/ARCHITECTURE.md)、[实验协议](docs/EXPERIMENT_PROTOCOL.md)、[开发路线](docs/ROADMAP.md) 和 [GitHub 发布说明](docs/PUBLISHING.md)。

## 相关工作与来源

- [BrowseComp-Plus](https://arxiv.org/abs/2508.06600)：计划复用其受控搜索与评测环境。
- [ReAct](https://arxiv.org/abs/2210.03629)：计划中的搜索执行范式。
- [ACE](https://arxiv.org/abs/2510.04618)：增量 playbook 对照。
- [ReasoningBank](https://arxiv.org/abs/2509.25140)：跨任务推理记忆对照。
- [Memento](https://arxiv.org/abs/2508.16153)、[GEPA](https://arxiv.org/abs/2507.19457)：相关机制参考。

本仓库目前未复制这些项目的源码。接入前应核对许可证、固定 commit，并记录修改。项目自身的开源许可证尚未选定；公开仓库并不自动授予开源许可。
