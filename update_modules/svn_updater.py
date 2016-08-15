import os
import shutil
from . import common

def create_repo(__base_repo_path, __repo_name, __svn_url):
	addon_repo_path = os.path.join(__base_repo_path, __repo_name)
	if (os.path.isdir(addon_repo_path)):
		shutil.rmtree(addon_repo_path)

	os.chdir(__base_repo_path)
	common.run_cmd('svn checkout %s %s' % (__svn_url, __repo_name))

def update_repo(__addon_repo_path, __repo_name):
	os.chdir(__addon_repo_path)
	common.run_cmd('svn update')