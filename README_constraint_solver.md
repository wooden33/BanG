# LLM Constraint Solver 说明文档

## 概述
LLM Constraint Solver是一个基于LLM的约束求解器，用于为被测函数和未覆盖路径生成输入变量的条件，帮助提高代码覆盖率。

## 功能特性
1. **基于路径的约束生成**：分析未覆盖路径并生成相应的输入条件
2. **与项目集成**：与Panta项目现有的配置系统和工作流程集成
3. **TOML模板支持**：使用可配置的TOML模板生成约束求解提示
4. **批量处理**：支持为多个未覆盖路径批量生成约束条件

## 主要组成部分

### 1. 约束求解器核心 (`src/panta/llm_constraint_solver.py`)
实现了约束求解的主要逻辑，包括：
- LLM调用
- 路径信息解析
- 提示词渲染
- 结果处理

### 2. 约束求解提示模板 (`src/panta/prompt_templates/java_templates/constraint_solving_prompt.toml`)
包含用于生成约束条件的系统提示和用户提示。

### 3. 配置加载系统 (`src/panta/config_loader.py`)
通过Dynaconf加载模板配置。

## 使用方法

### 基本使用
```python
from src.panta.llm_constraint_solver import LLMConstraintSolver
from src.panta.model_invocation.llm_invocation import LLMInvocation

# 初始化LLM调用器
llm_invoker = LLMInvocation("your-model-name")

# 创建约束求解器
solver = LLMConstraintSolver(llm_invoker)

# 被测函数源代码
source_code = """
def calculate_discount(price, quantity):
    discount = 0.0
    if price > 100:
        discount += 0.1  # 10% discount
    return discount
"""

# 未覆盖路径信息
uncovered_path = {
    "path": [
        {"statement": "def calculate_discount(price, quantity):", "conditional": None},
        {"statement": "    discount = 0.0", "conditional": None},
        {"statement": "    if price > 100:", "conditional": True},  # 未覆盖的分支
        {"statement": "        discount += 0.1", "conditional": None}
    ]
}

# 生成约束条件
constraints = solver.generate_constraints(source_code, uncovered_path)
print(f"Generated constraints: {constraints}")
```

### 批量处理
```python
# 多个未覆盖路径
uncovered_paths = [path1, path2, path3]
results = solver.batch_generate_constraints(source_code, uncovered_paths)

for path, constraints in results:
    print(f"Path constraints: {constraints}")
```

## 模板说明
约束求解模板位于`src/panta/prompt_templates/java_templates/constraint_solving_prompt.toml`，包含以下结构：

```toml
[constraint_solving_prompt]
system="""
你是一个代码覆盖约束求解专家...
"""

user="""
## Overview
你需要为函数生成输入条件...

## Source Code
Here is the source code...

## Uncovered Path Information
This path contains the following statements...
"""
```

## 输出示例
```
price > 100
```

## 与现有流程集成
约束求解器可以与现有的Panta工作流程集成，例如在`prompt_builder.py`中使用，为未覆盖路径生成约束条件并将其包含在测试生成提示中。
