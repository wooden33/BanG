import argparse
import configparser
import os
from .panta import Panta


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    confparser = configparser.ConfigParser()
    confparser.read(config_path)
    return confparser['default']


def config_to_namespace(config):
    return argparse.Namespace(
        project_directory=config.get('project_directory'),
        source_code_file=config.get('source_code_file'),
        test_code_file=config.get('test_code_file'),
        test_file_output_path=config.get('test_file_output_path'),
        code_coverage_report_path=config.get('code_coverage_report_path'),
        test_execution_command=config.get('test_execution_command'),
        test_dependency_command=config.get('test_dependency_command'),
        test_code_command_dir=config.get('test_code_command_dir'),
        included_files=config.get('included_files'),
        junit_version=config.getint('junit_version'),
        model=config.get('model'),
        coverage_type=config.get('coverage_type'),
        report_filepath=config.get('report_filepath'),
        target_coverage=config.getint('target_coverage'),
        maximum_iterations=config.getint('maximum_iterations'),
        no_coverage_increase_iterations=config.getint('no_coverage_increase_iterations'),
        enable_fixing=config.getint("enable_fixing"),
        run_symprompt=config.getboolean("run_symprompt"),
        prompt_type=config.get('prompt_type'),
        pick_two_paths=config.getboolean("pick_two_paths"),
        additional_instructions=config.get('additional_instructions')
    )


def main():
    config_parser = load_config()
    args = config_to_namespace(config_parser)
    panta = Panta(args)
    if args.run_symprompt:
        panta.run_symprompt()
    else:
        panta.run()


if __name__ == "__main__":
    main()
