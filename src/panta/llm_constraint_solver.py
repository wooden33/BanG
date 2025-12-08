#!/usr/bin/env python3
"""
LLM-based Constraint Solver for generating input variable conditions
to cover uncovered paths in the function under test.
"""

import logging
from typing import List, Dict, Any, Tuple
from jinja2 import Environment, StrictUndefined
from .model_invocation.llm_invocation import LLMInvocation
from .config_loader import get_settings
from .panta_logger import pantaLogger


class LLMConstraintSolver:
    """
    LLM-based constraint solver to generate input conditions for uncovered paths.
    """

    def __init__(self, llm_invoker: LLMInvocation):
        """
        Initialize the constraint solver.

        Args:
            llm_invoker: LLM invocation instance
        """
        self.logger = pantaLogger.initialize_logger(__name__)
        self.llm_invoker = llm_invoker

        # Load constraint solving prompt template
        self.template = self._load_prompt_template()
        self.jinja_env = Environment(undefined=StrictUndefined)

    def _load_prompt_template(self) -> Dict[str, str]:
        """
        Load the constraint solving prompt template using the existing config system.

        Returns:
            Dict[str, str]: System and user prompt templates
        """
        try:
            settings = get_settings()
            constraint_prompt = settings.constraint_solving_prompt

            if constraint_prompt:
                return {
                    "system": constraint_prompt.system,
                    "user": constraint_prompt.user
                }
            else:
                self.logger.warning("Constraint solving prompt template not found")
                return self._get_default_template()

        except Exception as e:
            self.logger.error(f"Failed to load constraint solving template: {str(e)}")
            return self._get_default_template()

    def _get_default_template(self) -> Dict[str, str]:
        """
        Get default prompt template as fallback.

        Returns:
            Dict[str, str]: Default system and user prompts
        """
        return {
            "system": "You are an expert in constraint solving for code coverage.",
            "user": """Analyze the following code and path to reach:
Code:
{{ source_code|trim }}

Path:
{{ path_info|trim }}

Generate simple input conditions:
"""
        }

    def _render_prompt(self, source_code: str, path_info: str) -> Dict[str, str]:
        """
        Render the constraint solving prompt using Jinja2.

        Args:
            source_code: Source code of the function under test
            path_info: String representation of the path information

        Returns:
            Dict[str, str]: Rendered system and user prompts
        """
        try:
            user_prompt = self.jinja_env.from_string(self.template["user"]).render(
                source_code=source_code,
                path_info=path_info
            )

            return {
                "system": self.template["system"],
                "user": user_prompt
            }
        except Exception as e:
            self.logger.error(f"Failed to render constraint solving prompt: {str(e)}")
            # Fallback to basic prompt without Jinja2
            return {
                "system": self.template["system"],
                "user": f"Analyze this code:\n{source_code}\n\nPath to reach:\n{path_info}\n\nGenerate input conditions:"
            }

    def generate_constraints(self, source_code: str, uncovered_path: Dict[str, Any]) -> str:
        """
        Generate input constraints for a single uncovered path.

        Args:
            source_code: Source code of the function under test
            uncovered_path: Detailed information about the uncovered path (from CFG analysis)

        Returns:
            str: Generated constraints
        """
        if not self.llm_invoker:
            self.logger.error("LLM invoker not initialized, cannot generate constraints")
            return ""

        try:
            # Convert path structure to readable string format
            path_repr = []
            if "path" in uncovered_path:
                for node in uncovered_path["path"]:
                    node_statements = [stmt.strip() for stmt in node['statement'].split("\n") if stmt.strip()]
                    for stmt in node_statements:
                        path_repr.append(stmt)

                    # Add conditional direction information if available
                    if node['conditional'] is not None:
                        cond_dir = " (True branch)" if node['conditional'] else " (False branch)"
                        path_repr[-1] += cond_dir

            path_info = "\n".join(path_repr)

            # Render the prompt
            prompt = self._render_prompt(source_code, path_info)
            self.logger.debug(f"Generated constraint prompt: {prompt}")

            # Call LLM and get response
            response = self.llm_invoker.invoke(prompt)
            constraints = response.strip()

            self.logger.info(f"Generated constraints: {constraints}")
            return constraints

        except Exception as e:
            self.logger.error(f"Error in generate_constraints: {str(e)}")
            return ""

    def batch_generate_constraints(self, source_code: str, uncovered_paths: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], str]]:
        """
        Batch generate input constraints for multiple uncovered paths.

        Args:
            source_code: Source code of the function under test
            uncovered_paths: List of uncovered paths

        Returns:
            List[Tuple[Dict[str, Any], str]]: Paths with their corresponding constraints
        """
        results = []
        for path in uncovered_paths:
            constraints = self.generate_constraints(source_code, path)
            results.append((path, constraints))
        return results


if __name__ == "__main__":
    # Simple test with mock LLM
    class MockLLM:
        def invoke(self, prompt):
            print("LLM Prompt:")
            print("=" * 50)
            print(prompt["system"])
            print(prompt["user"])
            print("=" * 50)
            print("Mock LLM Response:")
            return "price > 100"

    # Create test inputs
    test_code = """
def calculate_discount(price, quantity):
    discount = 0.0
    if price > 100:
        discount += 0.1  # 10% discount for expensive items
    return discount
"""

    test_path = {
        "path": [
            {"statement": "def calculate_discount(price, quantity):", "conditional": None},
            {"statement": "    discount = 0.0", "conditional": None},
            {"statement": "    if price > 100:", "conditional": True},
            {"statement": "        discount += 0.1", "conditional": None}
        ]
    }

    # Test the solver
    print("Testing LLM Constraint Solver")
    print("=" * 70)

    # Check if we can access the template
    try:
        solver = LLMConstraintSolver(MockLLM())
        constraints = solver.generate_constraints(test_code, test_path)
        print(f"\nGenerated Constraints: {constraints}")
        print("\nTest completed successfully!")
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
