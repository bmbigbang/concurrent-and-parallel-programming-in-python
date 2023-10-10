import threading

from queue import Empty

from sqlalchemy import create_engine
from sqlalchemy.sql import text


class SQLLiteScheduler(threading.Thread):
    def __init__(self, sqlite_queue, **kwargs):
        super(SQLLiteScheduler, self).__init__(**kwargs)
        self._sqlite_queue = sqlite_queue
        self.start()

    def run(self):
        while True:
            try:
                val = self._sqlite_queue.get(timeout=10)
            except Empty:
                print('Timeout reached in sqlite scheduler')
                break

            if val == 'DONE':
                break

            sql_lite_worker = SQLiteWorker(symbol=val[0], price=val[1])
            sql_lite_worker.insert_into_db()


class SQLiteWorker():
    def __init__(self, symbol, price):
        self._symbol = symbol
        self._price = price

        self._db = 'tutorial.db'
        self._engine = create_engine('sqlite:///' + self._db, echo=True)

    @staticmethod
    def _create_insert_query(self):
        SQL = ("INSERT INTO prices(symbol, price, extraction_time) VALUES "
               "(:symbol, :price, datetime('now'))")
        return SQL

    def insert_into_db(self):
        insert_query = self._create_insert_query(self)

        with self._engine.connect() as conn:
            conn.execute(text(insert_query), {"symbol": self._symbol, "price": self._price})
            conn.commit()
