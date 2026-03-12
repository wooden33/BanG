import argparse
import configparser
import os
from .panta import Panta


def load_config(config_file=None):
    if config_file is None:
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    else:
        # Support both absolute and relative paths
        if os.path.isabs(config_file):
            config_path = config_file
        else:
            config_path = os.path.join(os.path.dirname(__file__), config_file)
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
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
        solver_model=config.get('solver_model'),
        coverage_type=config.get('coverage_type'),
        report_filepath=config.get('report_filepath'),
        target_coverage=config.getint('target_coverage'),
        maximum_iterations=config.getint('maximum_iterations'),
        no_coverage_increase_iterations=config.getint('no_coverage_increase_iterations'),
        enable_fixing=config.getint("enable_fixing"),
        run_symprompt=config.getboolean("run_symprompt"),
        run_hits=config.getboolean("run_hits"),
        prompt_type=config.get('prompt_type'),
        use_constraints=config.getboolean("use_constraints"),
        use_backward_slice=config.getboolean("use_backward_slice"),
        fix_type=config.get('fix_type', None),
        pick_two_paths=config.getboolean("pick_two_paths"),
        additional_instructions=config.get('additional_instructions')
    )


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Panta - Automated Unit Test Generation')
    parser.add_argument('--config', '-c', type=str, default=None,
                        help='Path to configuration file (default: config.ini)')
    
    args = parser.parse_args()
    
    # Load configuration
    config_parser = load_config(args.config)
    config_args = config_to_namespace(config_parser)
    
    # Create and run Panta
    panta = Panta(config_args)
    if config_args.run_symprompt:
        panta.run_symprompt()
    elif config_args.run_hits:
        panta.run_hits()
    else:
        panta.run()


if __name__ == "__main__":
    main()
