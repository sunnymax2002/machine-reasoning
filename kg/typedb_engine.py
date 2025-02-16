# REF: https://github.com/typedb/typedb-docs/blob/3.x-master/drivers/modules/ROOT/partials/tutorials/python/sample.py

from typedb.driver import TypeDB, TransactionType, Credentials, DriverOptions
from enum import Enum

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
		# TODO: Is it secure to store credentials?
		self.cred = Credentials(config[self.K_USERNAME], config[self.K_PASSWORD])
		self.db_name = config[self.K_DB_NAME]

		# TODO: Add support for core db
		# Connect to cloud database
		with TypeDB.cloud_driver([self.server_addr], self.cred, DriverOptions(True, None)) as drv:
			if drv.databases.contains(self.db_name):
				drv.databases.get(self.db_name).delete()
			drv.databases.create(self.db_name)