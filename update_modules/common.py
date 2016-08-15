import os
import logging
import subprocess

def run_cmd(cmd, logger):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('ascii').strip()
    error = error.decode('ascii').strip()
    if (len(output) > 0):
        logger.info(output)
    if (len(error) > 0):
        logger.error(error)

def make_logger(log_folder, name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(os.path.join(log_folder, name + ".log"))
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

class BaseRepo:
    def __init__(self, base_repo_path, repo_name, repo_url):
        self.base_repo_path = base_repo_path
        self.addon_repo_path = os.path.join(base_repo_path, repo_name)
        self.repo_name = repo_name
        self.repo_url = repo_url
        self.logger = make_logger(base_repo_path, repo_name)

    def create_repo(self):
        raise("Not implemented.")
    def update_repo(self):
        raise("Not implemented.")
    def is_repo_updatable(self):
        raise("Not implemented.")
