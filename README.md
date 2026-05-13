# hello-my-agents
这是学习过程中构建的各种agentic工作流，是对agent的初步探索，更是个人学习的总结。


## 项目简介

### [基于AutoGen的自动编码助手](https://github.com/KANG99/hello-my-agents/blob/main/%E5%9F%BA%E4%BA%8EAutoGen%E7%9A%84%E8%87%AA%E5%8A%A8%E7%BC%96%E7%A0%81%E5%8A%A9%E6%89%8B.ipynb)
- 本项目利用AutoGen框架构建多智能体协作系统，实现自动化代码生成与调试。
- 支持多种编程语言，能够根据需求描述快速生成高质量代码片段。
- 集成了代码审查与优化功能，可自动检测潜在问题并提供改进建议。
- 通过对话式交互界面，用户可便捷地与AI助手沟通开发需求。
- 适用于快速原型开发、学习辅助及日常编程任务自动化场景。

以下为自动编码的网页内容：

<img src="https://github.com/KANG99/hello-my-agents/blob/main/Images/autogen_demo.png" title="某次自动编码生成的黄金看板" width=400 height=400>


### [爆款产品市场调研及海报生成](http://github.com/KANG99/hello-my-agents/blob/main/%E7%88%86%E6%AC%BE%E4%BA%A7%E5%93%81%E5%B8%82%E5%9C%BA%E8%B0%83%E7%A0%94%E5%8F%8A%E6%B5%B7%E6%8A%A5%E7%94%9F%E6%88%90.ipynb)
- 基于多智能体协作架构，实现从市场数据收集、竞品分析到用户画像生成的全链路自动化调研流程。
- 集成网络爬虫与API接口，实时获取电商平台、社交媒体的热销产品数据及用户评价信息。
- 运用自然语言处理技术自动分析市场趋势，识别潜在爆款特征并生成可视化数据报告。
- 结合AI图像生成能力，根据调研结果自动设计营销海报，支持多风格模板与品牌定制化需求。
- 适用于电商运营、品牌营销及产品策划等场景，大幅缩短市场调研周期并降低设计成本。

以下为生成的数据分析报告的部分内容：

<img src="https://github.com/KANG99/hello-my-agents/blob/main/Images/%E9%83%A8%E5%88%86%E5%88%86%E6%9E%90%E6%8A%A5%E5%91%8A%E5%86%85%E5%AE%B9.png" title="爆款产品数据分析报告部分内容" width=400 height=400>

### [多平台内容生成器](https://github.com/KANG99/hello-my-agents/blob/main/HelloDify-%E5%A4%9A%E5%B9%B3%E5%8F%B0%E5%86%85%E5%AE%B9%E7%94%9F%E6%88%90%E5%99%A8.yml)
-  根据Dify官方demo，动手搭建的多平台内容生成器。主要实现的功能：将一段普通文案，润色成适合在不同社交平台发布的个性化文案。
-  内容主要涉及：
    - 用户输入
    - 参数提取
    - IF/ELSE 条件分支
    - 列表操作
    - 文档提取
    - LLM 大模型（配置ollama提供本地llm服务，主要用到了llm glm-flash-4.7,qwen3.5:35b-a3b）
    - 迭代循环
    - 模板
    - 输出九大工作流节点
    - 复用了模型配置、多模态视觉、结构化输出、并行执行与 Jinja2 模板能力。
- 搭建平台：Dify本地平台。
    
部分结果如下：

<img src="https://github.com/KANG99/hello-my-agents/blob/main/Images/dify%20demo.png" title="dify多平台内容生成结果" width=400 height=400>


### [RAG四大名著问答系统](https://github.com/KANG99/hello-my-agents/blob/main/RAG%EF%BC%9A%E5%9B%9B%E5%A4%A7%E5%90%8D%E8%91%97%E9%97%AE%E7%AD%94%E7%B3%BB%E7%BB%9F.ipynb)
- 基于检索增强生成（RAG）技术构建的智能问答系统，目前只实现了红楼梦数据库的问答功能。
- 离线LLM模型为Qwen3-4B-Instruct-2507,使用Qwen3-Embedding-0.6B模型进行文本嵌入，将名著文本转换为高维向量表示。
- 采用Faiss向量数据库存储名著文本的语义向量，实现高效的相似度检索与上下文召回。
- 适用于文学研究、教育教学及传统文化普及等场景，为古典文学爱好者提供智能化的知识服务。
- 50道测试用例，测试结果如下：
<img src="https://github.com/KANG99/hello-my-agents/blob/main/Images/barplot.png" title="问答结果" width=400 height=400>
- 实际上还有较大提升空间，比如修改文档切分颗粒度，让LLM优化问题等方式。模型选择很关键，在做RAG之前，先测试一下模型的表现，不然都是坑。
    - [测试题目及结果](example results/hongloumeng_QA.numbers)
    - [gradio使用RAG问答部分结果展示](https://github.com/KANG99/hello-my-agents/blob/main/Images/RAGOutput.jpeg)
    - [gradio未用RAG问答部分结果展示](https://github.com/KANG99/hello-my-agents/blob/main/Images/NormalOutput.jpeg)


## 参考项目

- [agentic-ai](https://github.com/datawhalechina/agentic-ai)
- [autogen](https://github.com/microsoft/autogen)
- [hello-agents](https://github.com/datawhalechina/hello-agents)
- [AgentScope](https://docs.agentscope.io/)
- [Dify](https://docs.dify.ai/en/use-dify/getting-started/introduction)
