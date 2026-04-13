import yaml
import os
import sys

from typedb_engine import TypeDbEngine

# REF: https://stackoverflow.com/questions/4934806/how-can-i-find-scripts-directory
yaml_path = os.path.join(sys.path[0], "example.yaml")
with open(yaml_path) as stream:       
	config = yaml.safe_load(stream)

engine = TypeDbEngine(config)

engine.db_create()
engine.db_delete()

print('Done')