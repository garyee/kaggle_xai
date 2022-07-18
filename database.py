from sqlite3 import connect, Error
from kaggleEnums import filePath

databasePath = filePath+"kaggleSqlite.db"

currentConnection=None

sql_create_dataset_info = """ CREATE TABLE IF NOT EXISTS dataset_info (
                                    dataBaseRef text NOT NULL PRIMARY KEY,
                                    is_competition BOOLEAN NOT NULL CHECK (is_competition IN (0, 1)) DEFAULT 0,
                                    type TEXT CHECK( type IN ('Tabular','Image','Video','Text','DB','Time Series','Misc') ) DEFAULT NULL,
                                    tab_corr REAL NULL DEFAULT NULL,
                                    tab_interaction REAL NULL DEFAULT NULL,
                                    tab_features_total INTEGER NULL DEFAULT NULL,
                                    tab_cat_features INTEGER NULL DEFAULT NULL,
                                    tab_num_features INTEGER NULL DEFAULT NULL
                                    tab_goal text CHECK (goal IN ('classification','regression','misc')) DEFAULT NULL,
                                ); """

sql_create_kernel_info = """ CREATE TABLE IF NOT EXISTS kernel_info (
                                    kernelRef text NOT NULL PRIMARY KEY,
                                    dataBaseRef text NOT NULL PRIMARY KEY,
                                    hasBlackBoxModel BOOLEAN NOT NULL CHECK (hasBlackBoxModel IN (0, 1)) DEFAULT 0,
                                    hasGlassBoxModel BOOLEAN NOT NULL CHECK (hasBlackBoxModel IN (0, 1)) DEFAULT 0,
                                    Performance REAL NULL DEFAULT NULL,
                                    CONSTRAINT fk_dataBaseRef
                                        FOREIGN KEY (dataBaseRef)
                                        REFERENCES dataset_info (dataBaseRef)
                                ); """

sql_create_xai_methods = """ CREATE TABLE IF NOT EXISTS kernel_info (
                                    kernelRef text NOT NULL PRIMARY KEY,
                                    hasBlackBoxModel BOOLEAN NOT NULL CHECK (hasBlackBoxModel IN (0, 1)) DEFAULT 0,
                                    CONSTRAINT fk_kernelRef
                                        FOREIGN KEY (kernelRef)
                                        REFERENCES kernel_info (kernelRef)
                                ); """
def insertRowOrIncrementKernelCount(dataSetRef,is_competition):
    query="INSERT OR IGNORE INTO dataset_info (dataBaseRef,is_competition) VALUES ('"+dataSetRef+"', '"+str(is_competition)+"');"
    execute_write_query(query)

def getAllDataSetRefs():
    return execute_read_query("SELECT dataBaseRef FROM dataset_info WHEREis_competition=0")

def execute_many(query,data,connection=None):
    global currentConnection
    connectionToUse = currentConnection or connection
    if connectionToUse is None:
        raise Exception("Initialize DB-connection before using it!")
    cursor = currentConnection.cursor()
    try:
        cursor.executemany(query,data)
        currentConnection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_write_query(query,connection=None):
    global currentConnection
    connectionToUse = currentConnection or connection
    if connectionToUse is None:
        raise Exception("Initialize DB-connection before using it!")
    cursor = connectionToUse.cursor()
    try:
        cursor.execute(query)
        connectionToUse.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(query,connection=None):
    global currentConnection
    connectionToUse = currentConnection or connection
    if connectionToUse is None:
        raise Exception("Initialize DB-connection before using it!")
    cursor = connectionToUse.cursor()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")
    return []

# def create_tables(db_file):
#     conn = None
#     try:
#         conn = connect(databasePath)
#         execute_write_query(sql_create_dataset_info,conn)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()

def initConnection():
    global currentConnection
    try:
        currentConnection = connect(databasePath)
        execute_write_query(sql_create_dataset_info)
        execute_write_query(sql_create_kernel_info)
        execute_write_query(sql_create_xai_methods)
    except Error as e:
        print(e)

def closeConnection():
    global currentConnection
    if currentConnection:
        currentConnection.close()

