import logging
from .panta_logger import pantaLogger
from .config_loader import get_settings
from .templates import ADDITIONAL_INCLUDES_TEXT, ADDITIONAL_INSTRUCTIONS_TEXT, FAILED_TESTS_TEXT
from jinja2 import Environment, StrictUndefined
from .cfg.src.comex.codeviews.combined_graph.combined_driver import CombinedDriver
from .cfg_branch_analyzer import CFGBranchAnalyzer
import random

from .utils import read_file

MAX_TESTS_PER_RUN = 4


class PromptBuilder:

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
                 test_dependencies=""):
        if lines_missed is None:
            lines_missed = []
        if branch_missed is None:
            branch_missed = []
        if path_history is None:
            path_history = {}

        self.project_dir = project_dir
        self.source_file_name = source_code_file.split("/")[-1]
        self.test_file_name = test_code_file.split("/")[-1]
        self.source_file = read_file(source_code_file)
        self.test_file = read_file(test_code_file)
        self.code_coverage_report = code_coverage_report
        self.language = language

        cfg_driver = CombinedDriver(src_language=self.language, src_code=self.source_file)
        self.processed_source_code = cfg_driver.preprocessed_src_code
        self.cfg_obj = cfg_driver.file_obj
        self.cfg_node_to_line = cfg_driver.node_id_to_line_number
        self.line_to_cfg_node = cfg_driver.line_number_to_node_id
        self.lines_missed = lines_missed
        self.branch_missed = branch_missed
        self.path_history = path_history
        self.test_dependencies = test_dependencies

        # Initialize CFG branch analyzer
        self.cfg_branch_analyzer = CFGBranchAnalyzer(self.language, self.source_file)
        self.cfa_guided_methods_under_test = self.extract_cfa_info_for_each_method_under_test()

        self.logger = pantaLogger.initialize_logger(__name__)

        # add line numbers to each line in 'source_file'. start from 1
        self.source_file_numbered = "\n".join(
            [f"{i + 1} {line}" for i, line in enumerate(self.source_file.split("\n"))]
        )
        self.test_file_numbered = "\n".join(
            [f"{i + 1} {line}" for i, line in enumerate(self.test_file.split("\n"))]
        )

        # Conditionally fill in optional sections
        self.included_files = (
            ADDITIONAL_INCLUDES_TEXT.format(included_files=included_files)
            if included_files
            else ""
        )
        self.additional_instructions = (
            ADDITIONAL_INSTRUCTIONS_TEXT.format(
                additional_instructions=additional_instructions
            )
            if additional_instructions
            else ""
        )
        self.failed_test_runs_feedback = (
            FAILED_TESTS_TEXT.format(failed_test_runs=failed_test_runs)
            if failed_test_runs
            else ""
        )
        self.coverage_invalid_tests = coverage_invalid_tests
        self.failed_test_runs = failed_test_runs

    def identify_method_under_tests_with_missed_lines(self, method):
        lines = [
            line for node_id in method["method_declaration"]["nodes"] 
            for line in self.cfg_node_to_line[node_id]
        ]
        method_name = method["method_declaration"]["name"]
        cyc_complexity = method["method_declaration"]["complexity"]
        method_missed_lines = []
        method_missed_branches = []
        for line in self.lines_missed:
            if line in lines:
                method_missed_lines.append(line)
        for branch_line in self.branch_missed:
            if branch_line in lines:
                method_missed_branches.append(branch_line)
        return method_name, cyc_complexity, lines, method_missed_lines, method_missed_branches

    def generate_paths_to_be_covered(self, method, missed_lines, missed_branches):
        paths = method["paths"]
        candidate_paths = []
        method_label = (
            f"{method['method_declaration']['name']}_"
            f"{method['method_declaration']['id']}"
        )
        for index, path in enumerate(paths):
            path_label = f"{method_label}_{index}"
            path_node_ids = [node['id'] for node in path["path"]]
            path_lines = [
                line for node_id in path_node_ids 
                for line in self.cfg_node_to_line[node_id]
            ]
            path_covered_missed_lines = [value for value in missed_lines if value in path_lines]
            path_covered_missed_branches = [
                value for value in missed_branches if value in path_lines
            ]
            path_nodes = [
                (self.cfg_node_to_line[node['id']], node['statement'], node['conditional']) 
                for node in path["path"]
            ]
            if len(path_covered_missed_lines) or len(path_covered_missed_branches):
                path_conditions_str = ""

                for node in path_nodes:
                    node_lines = node[1].split("\n")
                    for i, line in enumerate(node[0]):
                        path_conditions_str += f"\n{line}: {node_lines[i]}"
                    if node[2] is not None:
                        path_conditions_str += f" is {node[2]}"
                missed_value = len(path_covered_missed_lines) + len(path_covered_missed_branches)
                candidate_paths.append((missed_value, path_lines, path_nodes, path_conditions_str, path_label))
                random.shuffle(candidate_paths)
        return candidate_paths

    def extract_cfa_info_for_each_method_under_test(self):
        # there may be multiple classes defined in the file, we focus on the outer class for now
        clz_obj = self.cfg_obj["class_objects"][0]
        methods_under_test = clz_obj["methods_under_test"]
        cfa_guided_methods = []
        for method in methods_under_test:
            name, complexity, lines, missed_lines, missed_branches = self.identify_method_under_tests_with_missed_lines(
                method)
            if complexity > 1:
                candidate_paths = self.generate_paths_to_be_covered(method, missed_lines, missed_branches)
            else:
                candidate_paths = []
            cfa_guided_methods.append((name, complexity, lines, missed_lines, candidate_paths))

        return sorted(cfa_guided_methods, key=lambda x: x[1], reverse=True)

    def pick_two_paths(self, candidate_paths, path_history, max_visit=10):

        if not candidate_paths:
            return None, None  # Handle empty input safely

        # Add visit count to each candidate path for comparison
        paths_with_visits = [
            (path, path_history.get(path[4], 0))  # path[4] is path_label
            for path in candidate_paths
        ]

        filtered_paths = [path for path in paths_with_visits if path[1] < max_visit]

        # Handle case where all paths are over-visited
        if not filtered_paths:
            return None, None

        # Exploitation: Pick highest-missed-value path
        highest_missed_path = max(filtered_paths, key=lambda x: x[0][0])[0]

        # Exploration: Pick least-visited path
        least_visited_path = max(filtered_paths, key=lambda x: -x[1])[0]  # Extract the path

        return highest_missed_path, least_visited_path

    def pick_path(self, candidate_paths, path_history, alpha=0.7):
        # candidate_paths: [(missed_value, path_lines, path_nodes, path_conditions_str, path_label)]
        # Add visit count to each candidate path for comparison
        if not candidate_paths:
            return None

        paths_with_visits = [
            (path, path_history.get(path[4], 0))  # path[4] is path_label
            for path in candidate_paths
        ]
        # Normalize missed_value for stable scoring
        max_missed_value = max((p[0] for p in candidate_paths), default=1)

        # Compute priority score
        prioritized_path = max(
            paths_with_visits,
            key=lambda x: (
                alpha * (x[0][0] / max_missed_value) + (1 - alpha) / (x[1] + 1),
                x[0][0]   # Tie-breaker
            )
        )[0]  # Extract the path

        return prioritized_path

    def build_prompt_cfa_guided(self, pick_two_paths=True) -> dict:
        """
        Replaces placeholders with the actual content of files read during initialization, and returns the formatted prompt.

        Parameters:
            None

        Returns:
            str: The formatted prompt string.
        """
        # generate branch coverage guidance
        branch_coverage_guidance = self.generate_branch_coverage_guidance()
        variables = {
            "source_file_name": self.source_file_name,
            "test_file_name": self.test_file_name,
            "source_file_numbered": self.source_file_numbered,
            "test_file_numbered": self.test_file_numbered,
            "source_file": self.source_file,
            "test_file": self.test_file,
            "test_dependencies": self.test_dependencies,
            "code_coverage_report": self.code_coverage_report,
            "coverage_invalid_tests_section": self.coverage_invalid_tests,
            "failed_tests_section": self.failed_test_runs_feedback,
            "additional_includes_section": self.included_files,
            "additional_instructions_text": self.additional_instructions,
            "language": self.language,
            "max_tests": MAX_TESTS_PER_RUN,
            "processed_source_code": self.processed_source_code,
            "branch_coverage_guidance": branch_coverage_guidance
        }

        environment = Environment(undefined=StrictUndefined)
        try:
            system_prompt = environment.from_string(
                get_settings().test_generation_cfg_guided_prompt.system
            ).render(variables)

            rendered_templates = ""
            for method in self.cfa_guided_methods_under_test:
                method_name = method[0]
                method_complexity = method[1]
                missed_lines = method[3]
                # print(method_name, missed_lines)
                # candidate_paths: [(missed_value, path_lines, path_nodes, path_conditions_str, path_label)]
                candidate_paths = method[4]
                rendered_template = ""
                if method_complexity > 1:
                    template_str = "\n=========\nPlease generate test case for method `{{ method_name }}` " \
                                   "to cover the path: {{ candidate_path }}"
                    if pick_two_paths:
                        highest_missed_path, least_visited_path = self.pick_two_paths(candidate_paths,
                                                                                      self.path_history)
                        if highest_missed_path and least_visited_path:
                            self.logger.info(
                                f"select the candidate path that covers the most missed lines for method {method_name}")
                            highest_path_label = highest_missed_path[4]
                            least_path_label = least_visited_path[4]
                            self.path_history[highest_path_label] = self.path_history.get(highest_path_label, 0) + 1
                            path_str = highest_missed_path[3]
                            rendered_template = environment.from_string(template_str).render(method_name=method_name,
                                                                                             candidate_path=path_str)
                            if least_path_label != highest_path_label:
                                self.logger.info(
                                    f"select another candidate path with the least time of visits for method {method_name}")
                                self.path_history[least_path_label] = self.path_history.get(least_path_label, 0) + 1
                                path_str = least_visited_path[3]
                                rendered_template += environment.from_string(template_str).render(method_name=method_name,
                                                                                                  candidate_path=path_str)
                    else:
                        prioritized_path = self.pick_path(candidate_paths, self.path_history)
                        if prioritized_path:
                            self.logger.info(
                                f"select the path that has highest priority score for method {method_name}")
                            path_label = prioritized_path[4]
                            self.path_history[path_label] = self.path_history.get(path_label, 0) + 1
                            path_str = prioritized_path[3]
                            rendered_template = environment.from_string(template_str).render(method_name=method_name,
                                                                                             candidate_path=path_str)
                else:
                    if missed_lines:
                        template_str_missed_lines = "\n=========\nPlease generate test case for method `{{ method_name }}` " \
                                                    "to cover missed lines: {{ missed_lines }}"

                        rendered_template = environment.from_string(template_str_missed_lines).render(
                            method_name=method_name, missed_lines=missed_lines)
                rendered_templates += rendered_template

            user_prompt = environment.from_string(
                get_settings().test_generation_cfg_guided_prompt.user
            ).render(variables, method_under_test=rendered_templates)

            self.logger.debug(f"system_prompt: {system_prompt}")
            self.logger.debug(f"user_prompt: {user_prompt}")
        except Exception as e:
            logging.error(f"Error rendering prompt: {e}")
            return {"system": "", "user": ""}

        # print(f"#### user_prompt:\n\n{user_prompt}")
        return {"system": system_prompt, "user": user_prompt}

    def get_current_path_history(self):
        return self.path_history

    def generate_branch_coverage_guidance(self) -> str:
        """
        generate branch coverage guidance
        """
        if not self.branch_missed:
            return ""
        # Use CFG branch analyzer to generate guidance information
        branch_guidance = self.cfg_branch_analyzer.generate_branch_coverage_prompt(self.branch_missed)

        if branch_guidance:
            return branch_guidance
        # If no CFG guidance, provide basic uncovered branch information
        basic_guidance = "\n=== Branch Coverage Information ===\n"
        basic_guidance += f"The following branch lines need coverage: {self.branch_missed}\n"
        basic_guidance += "Please generate test cases to cover these branch conditions.\n\n"
        return basic_guidance

    def build_prompt(self, coverage_enabled=False) -> dict:
        """
        Replaces placeholders with the actual content of files read during initialization, and returns the formatted prompt.

        Parameters:
            coverage_enabled

        Returns:
            str: The formatted prompt string.
        """
        variables = {
            "source_file_name": self.source_file_name,
            "test_file_name": self.test_file_name,
            "source_file_numbered": self.source_file_numbered,
            "test_file_numbered": self.test_file_numbered,
            "source_file": self.source_file,
            "test_file": self.test_file,
            "test_dependencies": self.test_dependencies,
            "code_coverage_report": self.code_coverage_report,
            "coverage_invalid_tests_section": self.coverage_invalid_tests,
            "failed_tests_section": self.failed_test_runs_feedback,
            "additional_includes_section": self.included_files,
            "additional_instructions_text": self.additional_instructions,
            "language": self.language,
            "max_tests": MAX_TESTS_PER_RUN,
        }
        environment = Environment(undefined=StrictUndefined)
        try:
            if coverage_enabled:
                system_prompt = environment.from_string(
                    get_settings().test_generation_prompt_with_code_coverage_report.system
                ).render(variables)
                user_prompt = environment.from_string(
                    get_settings().test_generation_prompt_with_code_coverage_report.user
                ).render(variables)
            else:
                system_prompt = environment.from_string(
                    get_settings().test_generation_prompt.system
                ).render(variables)
                user_prompt = environment.from_string(
                    get_settings().test_generation_prompt.user
                ).render(variables)

            self.logger.debug(f"system_prompt: {system_prompt}")
            self.logger.debug(f"user_prompt: {user_prompt}")
        except Exception as e:
            logging.error(f"Error rendering prompt: {e}")
            return {"system": "", "user": ""}

        # print(f"#### user_prompt:\n\n{user_prompt}")
        return {"system": system_prompt, "user": user_prompt}

    def build_prompt_custom(self, file) -> dict:
        variables = {
            "source_file_name": self.source_file_name,
            "test_file_name": self.test_file_name,
            "source_file_numbered": self.source_file_numbered,
            "test_file_numbered": self.test_file_numbered,
            "source_file": self.source_file,
            "test_file": self.test_file,
            "test_dependencies": self.test_dependencies,
            "code_coverage_report": self.code_coverage_report,
            "coverage_invalid_tests_section": self.coverage_invalid_tests,
            "additional_includes_section": self.included_files,
            "failed_tests_section": self.failed_test_runs_feedback,
            "additional_instructions_text": self.additional_instructions,
            "language": self.language,
            "max_tests": MAX_TESTS_PER_RUN,
        }
        environment = Environment(undefined=StrictUndefined)
        try:
            system_prompt = environment.from_string(
                get_settings().get(file).system
            ).render(variables)
            user_prompt = environment.from_string(get_settings().get(file).user).render(
                variables
            )
        except Exception as e:
            logging.error(f"Error rendering prompt: {e}")
            return {"system": "", "user": ""}

        return {"system": system_prompt, "user": user_prompt}

    def build_prompt_for_fixing(self, fix_type: str) -> dict:
        variables = {
            "source_file_name": self.source_file_name,
            "test_file_name": self.test_file_name,
            "source_file": self.source_file,
            "test_file": self.test_file,
            "test_dependencies": self.test_dependencies,
            "failed_test_runs": self.failed_test_runs,
            "language": self.language
        }
        environment = Environment(undefined=StrictUndefined)
        try:
            if fix_type == 'MCTS':
                system_prompt = environment.from_string(
                    get_settings().failed_test_prompt_with_MCTS.system
                ).render(variables)
                user_prompt = environment.from_string(get_settings().failed_test_prompt_with_MCTS.user).render(
                    variables
                )
            else:
                system_prompt = environment.from_string(
                    get_settings().failed_test_prompt.system
                ).render(variables)
                user_prompt = environment.from_string(get_settings().failed_test_prompt.user).render(
                    variables
                )
            self.logger.debug(f"system_prompt: {system_prompt}")
            self.logger.debug(f"user_prompt: {user_prompt}")
        except Exception as e:
            logging.error(f"Error rendering prompt: {e}")
            return {"system": "", "user": ""}

        return {"system": system_prompt, "user": user_prompt}
