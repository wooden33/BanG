import logging
import os


class pantaLogger:
    log_file = "panta.log"
    log_directory = None

    @classmethod
    def set_log_path(cls, prompt_type, llm_model, project_name, branch_analyzer=None):
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
        
        # Build directory name
        if branch_analyzer:
            directory_name = f"{prompt_type}_{llm_model}_{branch_analyzer}"
        else:
            directory_name = f"{prompt_type}_{llm_model}"
        
        # Create full log directory path
        cls.log_directory = os.path.join(project_root, "logs", directory_name)
        
        # Ensure directory exists
        os.makedirs(cls.log_directory, exist_ok=True)
        
        # Use project name as log filename to avoid multi-threading conflicts
        log_filename = f"{project_name}.log"
        cls.log_file = os.path.join(cls.log_directory, log_filename)

    @classmethod
    def initialize_logger(cls, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        if not logger.handlers:
            file_handler = logging.FileHandler(cls.log_file, mode="w")
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            # Stream handler for console output
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            stream_handler.setFormatter(stream_formatter)
            logger.addHandler(stream_handler)

        return logger
