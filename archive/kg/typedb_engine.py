# REF: https://github.com/typedb/typedb-docs/blob/3.x-master/drivers/modules/ROOT/partials/tutorials/python/sample.py

from enum import Enum
import os
import sys
import json

from typedb.driver import TypeDB, TransactionType, Credentials, DriverOptions

class TypeDbEngine:
	class DbType(Enum):
		Cloud = 1
		Core = 2

	K_SERVER_ADDR = 'SERVER_ADDR'
	K_DB_TYPE = 'DB_TYPE'
	K_USERNAME = 'USERNAME'
	K_PASSWORD = 'PASSWORD'
	K_DB_NAME = 'DB_NAME'
	def __init__(self, config: dict):
		self.server_addr = config[self.K_SERVER_ADDR]
		self.db_type = config[self.K_DB_TYPE]
		# TODO: Is it secure to store credentials in memory?
		self.cred = Credentials(config[self.K_USERNAME], config[self.K_PASSWORD])
		self.db_name = config[self.K_DB_NAME]

		# Schema dependency dict
		p = os.path.join(sys.path[0], "ontology/schemas.json")
		with open(p, 'r') as file:
			self.schemas_dict = json.load(file)

		# Lazy loading of typedb_driver
		self.typedb_drv = None

	def _get_typedb_driver(self):
		# Connect to server
		if self.typedb_drv is None:
			# TODO: Add support for core db
			self.typedb_drv = TypeDB.cloud_driver([self.server_addr], self.cred, DriverOptions(True, None))
		elif not self.typedb_drv.is_open():
			# TODO: how to reconnect, instead of recreating?
			self.typedb_drv = TypeDB.cloud_driver([self.server_addr], self.cred, DriverOptions(True, None))

		return self.typedb_drv
	
	def _get_db_name(self, db_name: str):
		return self.db_name if db_name is None else db_name

	def db_create(self, db_name: str = None):
		dbn = self._get_db_name(db_name)
		drv = self._get_typedb_driver()
		if drv.databases.contains(dbn):
			raise Exception("Database already exists")
		drv.databases.create(dbn)

	def db_delete(self, db_name: str = None):
		dbn = self._get_db_name(db_name)
		drv = self._get_typedb_driver()
		if not drv.databases.contains(dbn):
			raise Exception("Database doesn't exists")
		drv.databases.get(dbn).delete()

	def close_server_connection(self):
		if self.typedb_drv is not None and self.typedb_drv.is_open():
			self.typedb_drv.close()

	def schema_add(ontology: str):
		"Adds specified ontology and its dependencies to the schema"
		raise NotImplementedError()
	
	def schema_add_raw(tql_path: str):
		# TODO: Use file handle instead of string to allow in memory files
		"Adds schema based on specified TypeQL query file"
		raise NotImplementedError()
	
	def ontology_add(ontology: dict):
		"Augments core ontology map using specified dictionary"
		raise NotImplementedError()
	
	def db_write():
		"Writes to db based on specified TypeQL query, but doesn't allow any schema edits"
		raise NotImplementedError()