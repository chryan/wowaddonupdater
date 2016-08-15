import os
import shutil
from . import common

class GitRepo(common.BaseRepo):
    def __init__(self, *args, **kwargs):
        super(GitRepo, self).__init__(*args, **kwargs)

    def create_repo(self):
        if (os.path.isdir(self.addon_repo_path)):
            shutil.rmtree(self.addon_repo_path)
    
        os.chdir(self.base_repo_path)
        common.run_cmd('git clone %s %s' % (self.repo_url, self.repo_name), self.logger)
    
    def update_repo(self):
        os.chdir(self.addon_repo_path)
        common.run_cmd('git fetch --all', self.logger)
        common.run_cmd('git pull --rebase', self.logger)

    def is_repo_updatable(self):
        return os.path.isdir(os.path.join(self.addon_repo_path, '.git'))