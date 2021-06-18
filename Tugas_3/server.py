import rpyc                                       # rpyc - library koneksi
from rpyc.utils.helpers import classpartial
from rpyc.utils.server import ThreadedServer
from beautifultable import BeautifulTable
from sqlite3 import Connection, Cursor, connect


class Sqlite():
  def __init__(self, database: str):                        # inisiasi
    self.connection: Connection = connect(database)         
    self.cursor: Cursor = self.connection.cursor()          

  def run_query(self, query: str) -> list:                  # run query
    self.cursor.execute(query)

    return self.cursor.fetchall()

# sqlite
class SqliteService(rpyc.Service):
  def __init__(self, database: str):                        # inisiasi
    self.sqlite_service = Sqlite(database)

  def exposed_rawquery(self, query: str) -> list:           # exposed rawquery   
    return self.sqlite_service.run_query(query)

  def exposed_tabquery(self, query: str) -> str:            # exposed tabquery
    result = self.sqlite_service.run_query(query)

    table = BeautifulTable()                                # using BeautifulTable
    for row in result:                                      # append rows from db to table
      table.rows.append(row)

    # rows header (S + number)
    table.rows.header = ["S"+str(i) for i in range(1, len(result) + 1)]
    
    # colums header (deskripsi kolom)
    table.columns.header = [description[0] for description in self.sqlite_service.cursor.description]

    return table

  def exposed_quit(self) -> None:
    exit()


if __name__ == "__main__":

  
  service = classpartial(SqliteService, "data.db")
  server = ThreadedServer(service, port=1060)
  
  server.start()