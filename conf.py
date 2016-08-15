import json

class settings:
    def __init__(self, json_file):
        with open(json_file) as json_data:
            table = json.load(json_data)

            self.all_repos = table['all_repos']
            self.base_repo_path = table['base_repo_path']
            self.output_addon_path = table['output_addon_path']