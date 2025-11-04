import logging
from .panta_logger import pantaLogger
from .config_loader import get_settings
from .templates import ADDITIONAL_INCLUDES_TEXT, ADDITIONAL_INSTRUCTIONS_TEXT, FAILED_TESTS_TEXT
from jinja2 import Environment, StrictUndefined
from .cfg.src.comex.codeviews.combined_graph.combined_driver import CombinedDriver
from .cfg_branch_analyzer import CFGBranchAnalyzer
from .prompt_builder import PromptBuilder
from .file_access_interface import FileAccessInterface
from .model_invocation.tool_calling_llm import ToolCallingLLMInvocation, ToolCallingAzureOpenAIInvocation
import random
import os
from typing import Dict, Any, Optional

from .utils import read_file

MAX_TESTS_PER_RUN = 4


class EnhancedPromptBuilder(PromptBuilder):
    """
    增强版的PromptBuilder，支持LLM自主查看文件的能力
    """
    
    def __init__(self,
                 project_dir: str,
                 source_code_file: str,
                 test_code_file: str,
                 code_coverage_report: str = "",
                 included_files: str = "",
                 additional_instructions: str = "",
                 failed_test_runs: str = "",
                 coverage_invalid_tests: str = "",
                 language: str = "python",
                 lines_missed=None,
                 branch_missed=None,
                 path_history=None,
                 test_dependencies="",
                 enable_file_access=True):
        
        # 调用父类构造函数
        super().__init__(
            project_dir=project_dir,
            source_code_file=source_code_file,
            test_code_file=test_code_file,
            code_coverage_report=code_coverage_report,
            included_files=included_files,
            additional_instructions=additional_instructions,
            failed_test_runs=failed_test_runs,
            coverage_invalid_tests=coverage_invalid_tests,
            language=language,
            lines_missed=lines_missed,
            branch_missed=branch_missed,
            path_history=path_history,
            test_dependencies=test_dependencies
        )
        
        # 初始化文件访问接口
        self.enable_file_access = enable_file_access
        if enable_file_access:
            self.file_access = FileAccessInterface(project_dir)
        else:
            self.file_access = None
    
    def setup_llm_with_file_access_tools(self, llm_invoker):
        """
        为LLM设置文件访问工具
        """
        if not self.enable_file_access or not self.file_access:
            return llm_invoker
        
        # 如果LLM不支持工具调用，返回原始invoker
        if not isinstance(llm_invoker, (ToolCallingLLMInvocation, ToolCallingAzureOpenAIInvocation)):
            return llm_invoker
        
        # 注册文件访问工具
        llm_invoker.register_tool(
            name="list_directory",
            func=self.file_access.list_directory,
            description="List files and directories in a given path",
            parameters={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The directory path to list (relative to project root)"
                    },
                    "recursive": {
                        "type": "boolean",
                        "description": "Whether to list recursively",
                        "default": False
                    }
                },
                "required": ["path"]
            }
        )
        
        llm_invoker.register_tool(
            name="search_files",
            func=self.file_access.search_files,
            description="Search for files by name pattern or content",
            parameters={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "The search pattern (filename or content)"
                    },
                    "search_type": {
                        "type": "string",
                        "enum": ["filename", "content"],
                        "description": "Type of search to perform"
                    },
                    "file_extensions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "File extensions to include in search"
                    }
                },
                "required": ["pattern", "search_type"]
            }
        )
        
        llm_invoker.register_tool(
            name="get_file_content",
            func=self.file_access.get_file_content,
            description="Get the content of a specific file",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The file path (relative to project root)"
                    },
                    "start_line": {
                        "type": "integer",
                        "description": "Starting line number (1-based, optional)"
                    },
                    "end_line": {
                        "type": "integer",
                        "description": "Ending line number (1-based, optional)"
                    }
                },
                "required": ["file_path"]
            }
        )
        
        llm_invoker.register_tool(
            name="search_in_file",
            func=self.file_access.search_in_file,
            description="Search for specific content within a file",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The file path (relative to project root)"
                    },
                    "pattern": {
                        "type": "string",
                        "description": "The search pattern"
                    },
                    "context_lines": {
                        "type": "integer",
                        "description": "Number of context lines to include",
                        "default": 3
                    }
                },
                "required": ["file_path", "pattern"]
            }
        )
        
        llm_invoker.register_tool(
            name="get_class_info",
            func=self.file_access.get_class_info,
            description="Get information about classes in a file",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The file path (relative to project root)"
                    }
                },
                "required": ["file_path"]
            }
        )
        
        llm_invoker.register_tool(
            name="get_method_info",
            func=self.file_access.get_method_info,
            description="Get information about methods in a file",
            parameters={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "The file path (relative to project root)"
                    }
                },
                "required": ["file_path"]
            }
        )
        
        return llm_invoker
    
    def build_enhanced_prompt_with_file_access(self, coverage_enabled=False) -> dict:
        """
        构建增强版提示，包含文件访问指导
        """
        # 获取基础提示
        base_prompt = self.build_prompt(coverage_enabled)
        
        if not self.enable_file_access:
            return base_prompt
        
        # 添加文件访问指导
        file_access_guidance = """
## File Access Capabilities

You have access to the following file operations to help you generate better unit tests:

1. **list_directory(path, recursive=False)**: List files and directories in a given path
2. **search_files(pattern, search_type, file_extensions=None)**: Search for files by name or content
3. **get_file_content(file_path, start_line=None, end_line=None)**: Get file content with optional line range
4. **search_in_file(file_path, pattern, context_lines=3)**: Search for specific content within a file
5. **get_class_info(file_path)**: Get information about classes in a file
6. **get_method_info(file_path)**: Get information about methods in a file

### Usage Guidelines:

- Use these tools to explore the codebase and understand the context better
- Look for related classes, interfaces, and dependencies
- Examine existing test patterns and conventions
- Find utility classes or helper methods that might be useful
- Understand the project structure and naming conventions
- Look for configuration files, constants, or enums that might be relevant

### Best Practices:

1. Start by exploring the project structure to understand the codebase organization
2. Look for existing test files to understand testing patterns and conventions
3. Search for related classes and interfaces that the target class depends on
4. Examine utility classes and helper methods that might be useful for testing
5. Check for configuration files or constants that might affect the behavior
6. Use the file access tools strategically - don't just read everything, focus on what's relevant

Remember: The goal is to generate comprehensive, high-quality unit tests that cover edge cases and follow the project's testing conventions.
"""
        
        # 将文件访问指导添加到系统提示中
        enhanced_system_prompt = base_prompt["system"] + "\n\n" + file_access_guidance
        
        return {
            "system": enhanced_system_prompt,
            "user": base_prompt["user"]
        }
    
    def build_enhanced_prompt_cfa_guided(self, pick_two_paths=True) -> dict:
        """
        构建增强版CFA指导提示，包含文件访问能力
        """
        # 获取基础CFA提示
        base_prompt = self.build_prompt_cfa_guided(pick_two_paths)
        
        if not self.enable_file_access:
            return base_prompt
        
        # 添加文件访问指导（简化版，因为CFA提示已经比较复杂）
        file_access_guidance = """

## Additional File Access Tools Available

You can use the following tools to explore the codebase and gather more context:
- list_directory(path): Explore project structure
- search_files(pattern, search_type): Find related files
- get_file_content(file_path): Read specific files
- search_in_file(file_path, pattern): Search within files
- get_class_info(file_path): Get class information
- get_method_info(file_path): Get method information

Use these tools strategically to understand dependencies, find test patterns, and gather context for better test generation.
"""
        
        # 将文件访问指导添加到系统提示中
        enhanced_system_prompt = base_prompt["system"] + file_access_guidance
        
        return {
            "system": enhanced_system_prompt,
            "user": base_prompt["user"]
        }
    
    def get_project_overview(self) -> str:
        """
        获取项目概览信息，用于帮助LLM理解项目结构
        """
        if not self.file_access:
            return ""
        
        try:
            # 获取项目根目录结构
            root_structure = self.file_access.list_directory(".", recursive=False)
            
            # 查找主要的源代码目录
            source_dirs = []
            for item in root_structure:
                if item['type'] == 'directory' and item['name'] in ['src', 'lib', 'app', 'source']:
                    source_dirs.append(item['name'])
            
            # 查找测试目录
            test_dirs = []
            for item in root_structure:
                if item['type'] == 'directory' and ('test' in item['name'].lower() or 'spec' in item['name'].lower()):
                    test_dirs.append(item['name'])
            
            overview = f"""
Project Structure Overview:
- Root directory: {self.project_dir}
- Source directories: {', '.join(source_dirs) if source_dirs else 'Not found'}
- Test directories: {', '.join(test_dirs) if test_dirs else 'Not found'}
- Language: {self.language}
- Target source file: {self.source_file_name}
- Target test file: {self.test_file_name}
"""
            return overview
            
        except Exception as e:
            self.logger.warning(f"Failed to get project overview: {e}")
            return ""