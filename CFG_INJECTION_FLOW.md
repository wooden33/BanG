# CFG注入机制详解

## 1. CFG注入的完整数据流

```
源代码 → AST解析 → CFG图构建 → 分支分析 → 提示注入 → 测试生成
```

## 2. 详细注入步骤

### 步骤1：源代码解析
```python
# 在CFGDriver中
self.parser = ParserDriver(src_language, src_code).parser
self.root_node = self.parser.root_node
```
- 使用Tree-sitter解析源代码
- 生成抽象语法树(AST)
- 提取语言特定的语法结构

### 步骤2：CFG图构建
```python
# 在CFGDriver中
self.CFG = self.CFG_map[self.src_language](
    self.src_language,
    self.src_code,
    self.properties,
    self.root_node,
    self.parser,
)
```
- 根据AST构建控制流图
- 识别控制流节点（if、while、for等）
- 建立节点间的控制流边

### 步骤3：分支信息提取
```python
# 在CFGBranchAnalyzer中
for edge in self.graph.edges():
    source_node, target_node = edge
    edge_label = self.cfg_edge_map.get((source_node, target_node))
    
    if edge_label in ['pos_next', 'neg_next']:
        # 条件分支
        branch_info['conditional_branches'].append({...})
```
- 遍历CFG图的所有边
- 识别不同类型的分支
- 提取分支的源代码信息

### 步骤4：分支分析
```python
# 在CFGBranchAnalyzer中
def _extract_conditional_branches(self) -> List[Dict]:
    conditional_branches = []
    for edge in self.graph.edges():
        # 分析条件分支
        if edge_label in ['pos_next', 'neg_next']:
            # 提取分支信息
```
- 分析条件分支的true/false路径
- 识别循环分支的进入/退出条件
- 分析异常处理分支

### 步骤5：测试条件生成
```python
# 在CFGBranchAnalyzer中
def _generate_test_conditions(self, branch: Dict) -> List[str]:
    conditions = []
    statement = branch['statement']
    
    if 'if' in statement.lower():
        # 提取条件表达式
        condition = statement[statement.find('(')+1:statement.find(')')]
        conditions.append(f"Test case where condition '{condition}' evaluates to True")
        conditions.append(f"Test case where condition '{condition}' evaluates to False")
```
- 为每个分支生成具体的测试条件
- 提供true/false路径的测试建议
- 生成边界条件测试建议

### 步骤6：CFG信息注入到提示
```python
# 在PromptBuilder中
def generate_branch_coverage_guidance(self) -> str:
    branch_guidance = self.cfg_branch_analyzer.generate_branch_coverage_prompt(self.branch_missed)
    return branch_guidance
```
- 将CFG分析结果转换为自然语言描述
- 注入到LLM提示中
- 指导LLM生成针对性的测试用例

## 3. CFG注入的关键组件

### 3.1 CFGDriver
- **作用**：构建控制流图
- **输入**：源代码
- **输出**：CFG图结构

### 3.2 CFGBranchAnalyzer
- **作用**：分析CFG中的分支信息
- **输入**：CFG图结构
- **输出**：分支分析结果

### 3.3 PromptBuilder
- **作用**：将CFG信息注入到LLM提示
- **输入**：分支分析结果
- **输出**：增强的测试生成提示

### 3.4 UnitTestGenerator
- **作用**：使用CFG信息生成测试
- **输入**：增强的提示
- **输出**：针对性的测试用例

## 4. CFG注入的时机

### 4.1 初始化时注入
```python
# 在PromptBuilder.__init__中
self.cfg_branch_analyzer = CFGBranchAnalyzer(self.language, self.source_file)
```

### 4.2 测试生成时注入
```python
# 在Panta.run()中
if self.test_gen.branch_missed and len(self.test_gen.branch_missed) > 0:
    branch_tests_dict, branch_token_count = self.test_gen.generate_branch_focused_tests()
```

### 4.3 提示构建时注入
```python
# 在build_prompt_cfa_guided中
branch_coverage_guidance = self.generate_branch_coverage_guidance()
variables["branch_coverage_guidance"] = branch_coverage_guidance
```

## 5. CFG注入的效果

### 5.1 提高分支覆盖率
- 识别未覆盖的分支
- 生成针对性的测试用例
- 覆盖true/false路径

### 5.2 优化测试质量
- 基于CFG结构生成测试
- 考虑控制流依赖关系
- 生成更全面的测试用例

### 5.3 智能测试生成
- 自动识别复杂分支逻辑
- 生成边界条件测试
- 处理异常情况测试

## 6. CFG注入的配置

### 6.1 分支覆盖阈值
```python
# 在Panta类中
if self.test_gen.branch_missed and len(self.test_gen.branch_missed) > 0:
    # 触发分支覆盖优化
```

### 6.2 提示模板配置
```yaml
# 在prompt_templates/java_templates/branch_coverage_prompt.yaml中
system: |
  你是一个专业的单元测试生成器，专门负责生成高质量的测试用例来提高代码的分支覆盖率。
  ...
```

## 7. CFG注入的扩展性

### 7.1 自定义分支分析器
```python
class CustomBranchAnalyzer(CFGBranchAnalyzer):
    def _generate_test_conditions(self, branch):
        # 自定义测试条件生成逻辑
        pass
```

### 7.2 集成其他分析工具
```python
def integrate_static_analysis_results(self, analysis_results):
    # 将静态分析结果与CFG分析结合
    pass
```

## 总结

CFG注入机制通过以下方式工作：

1. **解析阶段**：将源代码解析为AST
2. **构建阶段**：从AST构建控制流图
3. **分析阶段**：分析CFG中的分支信息
4. **注入阶段**：将CFG信息注入到测试生成提示中
5. **生成阶段**：基于CFG信息生成针对性的测试用例

这种机制使得Panta能够：
- 智能识别代码的分支结构
- 生成更有针对性的测试用例
- 显著提高分支覆盖率
- 优化测试生成的质量和效率
