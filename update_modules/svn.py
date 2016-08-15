import os
import shutil
from . import common

class SvnRepo(common.BaseRepo):
    def __init__(self, *args, **kwargs):
        super(SvnRepo, self).__init__(*args, **kwargs)

    def create_repo(self):
        if (os.path.isdir(self.addon_repo_path)):
            shutil.rmtree(self.addon_repo_path)

        os.chdir(self.base_repo_path)
        common.run_cmd('svn checkout %s %s' % (self.repo_url, self.repo_name), self.logger)

    def update_repo(self):
        os.chdir(self.addon_repo_path)
        common.run_cmd('svn update', self.logger)

    def is_repo_updatable(self):
        return os.path.isdir(os.path.join(self.addon_repo_path, '.svn'))