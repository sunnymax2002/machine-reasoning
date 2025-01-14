# REF: https://typedb.com/docs/drivers/2.x/python/

import os
os.add_dll_directory(r"C:\Program Files\Python313\DLLs")

from typedb import driver

from typedb.driver import TypeDB, SessionType, TransactionType

DB_NAME = "access-management-db"
SERVER_ADDR = "127.0.0.1:1729"

with TypeDB.core_driver(SERVER_ADDR) as driver:
    if driver.databases.contains(DB_NAME):
        driver.databases.get(DB_NAME).delete()
    driver.databases.create(DB_NAME)

    with driver.session(DB_NAME, SessionType.SCHEMA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            tx.query.define("define person sub entity;")
            tx.query.define("define name sub attribute, value string; person owns name;")
            tx.commit()

    with driver.session(DB_NAME, SessionType.DATA) as session:
        with session.transaction(TransactionType.WRITE) as tx:
            tx.query.insert("insert $p isa person, has name 'Alice';")
            tx.query.insert("insert $p isa person, has name 'Bob';")
            tx.commit()
        with session.transaction(TransactionType.READ) as tx:
            results = tx.query.fetch("match $p isa person; fetch $p: name;")
            for json in results:
                print(json)