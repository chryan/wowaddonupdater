import logging
import multiprocessing
import os
import subprocess
import shutil

from update_modules import git, svn
from conf import settings

settings_file = "settings.json"

def get_repo(base_repo_path, repo_name, repo_url):
    class_type = None
    ## TODO: Do better URL parsing here
    if "git" in repo_url:
        class_type = git.GitRepo
    elif "svn" in repo_url:
        class_type = svn.SvnRepo

    if class_type is not None:
        return class_type(base_repo_path, repo_name, repo_url)

    return None

def create_copy_task(__addon_repo_path, __output_path, __append_output_path):
    copy_files = []
    make_dirs = set()
    for root, dirs, files in os.walk(__addon_repo_path):
        for name in files:
            input_file = os.path.join(root, name)
            relative_file = os.path.relpath(input_file, __addon_repo_path)

            if relative_file[0] == '.':
                continue

            output_file = os.path.join(__output_path, __append_output_path, relative_file)
            output_file_dir = os.path.dirname(output_file)
            if not os.path.isdir(output_file_dir):
                make_dirs.add(output_file_dir)

            copy_files.append((input_file, output_file))
    return (list(make_dirs), copy_files)

def handle_repo_worker(repo_vals, base_repo_path, output_addon_path):
    repo_name        = repo_vals[0]
    repo_url         = repo_vals[1]

    #logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')
    repo = get_repo(base_repo_path, repo_name, repo_url)

    if repo is None:
        print ("Invalid repo type for %s." % repo_name)
        return None

    # check if repo exists
    if repo.is_repo_updatable():
        print ("Updating %s..." % repo_name)
        repo.update_repo()
        print ("Update %s complete!" % repo_name)
    else:
        print ("Downloading %s..." % repo_name)
        repo.create_repo()
        print ("Download %s complete!" % repo_name)

    # Check if our root repo directory is the contents of our mod
    check_toc_file = os.path.join(repo.addon_repo_path, "%s.toc" % repo_name)
    append_output_path = ""
    if (os.path.isfile(check_toc_file)):
        append_output_path = repo_name

    return create_copy_task(repo.addon_repo_path, output_addon_path, append_output_path)

def update_addons_and_get_copytasks(all_repos, base_repo_path, output_addon_path):
    update_process_pool = multiprocessing.Pool(processes=16)

    jobs = []
    for repo in all_repos:
        res = update_process_pool.apply_async(handle_repo_worker, (repo,base_repo_path,output_addon_path,))
        jobs.append (res)

    update_process_pool.close()
    update_process_pool.join()

    copy_tasks = []
    for job in jobs:
        result = job.get()
        if (result is not None):
            copy_tasks.append(result)

    return copy_tasks

def init_paths(base_repo_path, output_addon_path):
    if not os.path.isdir(base_repo_path):
        os.makedirs(base_repo_path)
    if not os.path.isdir(output_addon_path):
        os.makedirs(output_addon_path)

# Remove all addons in our Interfaces folder
def clean_output_path(__addon_path):
    for d in os.listdir(__addon_path):
        if d[0] == '.':
            continue
        if "Blizzard_" not in d:
            shutil.rmtree(os.path.join(__addon_path, d))

def run_update():
    s = settings(settings_file)

    init_paths(s.base_repo_path, s.output_addon_path)
    clean_output_path(s.output_addon_path)

    copy_tasks = update_addons_and_get_copytasks(s.all_repos, s.base_repo_path, s.output_addon_path)

    dir_process_pool = multiprocessing.Pool(processes=16)
    file_process_pool = multiprocessing.Pool(processes=16)

    for (make_dirs, _) in copy_tasks:
        for dirname in make_dirs:
            dir_process_pool.apply_async(os.makedirs, (dirname,))

    dir_process_pool.close()
    dir_process_pool.join()

    for (_, copy_files) in copy_tasks:
        for inoutfiles in copy_files:
            file_process_pool.apply_async(shutil.copyfile, inoutfiles)

    file_process_pool.close()
    file_process_pool.join()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    run_update()