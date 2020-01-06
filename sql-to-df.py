import concurrent.futures
import pandas as pd
import pyodbc


class Query(object):
    """Query and SQL statement

    Property:
        data: SQL output (pandas.DataFrame)
    """
    _data = None

    def __init__(self, server, database, query, startup_query=False,
                 timeout=60):
        "timeout is in seconds"
        self.server = server
        self.database = database
        self.query = query
        self.timeout = timeout
        self.__sql_connect_phrase = 'DRIVER={SQL Server};SERVER=' + self.server\
                                    + ';DATABASE=' + self.database\
                                    + ';Trusted_Connection=yes'
        if startup_query:
            self.getsql()

    def getsql(self, force=False):
        """Read SQL data and assign to dataframe

        Returns
        -------
        pandas.DataFrame
        """
        if self._data is None or force:
            with pyodbc.connect(self.__sql_connect_phrase) as sql_connection:
                if self.timeout is not None:
                    with concurrent.futures.ThreadPoolExecutor(
                            max_workers=1) as executor:
                        future = executor.submit(lambda: pd.read_sql(self.query, sql_connection))
                        self._data = future.result(timeout=self.timeout)
                else:
                    self._data = lambda: pd.read_sql(self.query, sql_connection)
        return self._data


df = Query('server', 'database', """

    SELECT TOP 10 *
    FROM fruit_table ft

    """).getsql()
