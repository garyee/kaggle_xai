from sqlite3 import connect, Error

databaseBasePath='/content/drive/MyDrive/Colab/Kaggle/'
databasePath = databaseBasePath+"kaggleSqlite.db"

currentConnection=None

sql_create_dataset_info = """ CREATE TABLE IF NOT EXISTS dataset_info (
                                    dataBaseRef text NOT NULL PRIMARY KEY,
                                    is_competition BOOLEAN NOT NULL CHECK (is_competition IN (0, 1)) DEFAULT 0,
                                    type TEXT CHECK( type IN ('Tabular','Image','Video','Text','DB','Misc') ) DEFAULT NULL,
                                    Tab_corr REAL NULL DEFAULT NULL,
                                    Tab_interaction REAL NULL DEFAULT NULL,
                                    Tab_features_total INTEGER NULL DEFAULT NULL,
                                    Tab_cat_features INTEGER NULL DEFAULT NULL,
                                    Tab_num_features INTEGER NULL DEFAULT NULL
                                ); """
def insertRowOrIncrementKernelCount(dataSetRef,is_competition):
    query="INSERT INTO dataset_info (dataBaseRef,is_competition) VALUES ('"+dataSetRef+"', '"+str(is_competition)+"');"
    print(query)
    execute_query(query)


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


def execute_query(query,connection=None):
    global currentConnection
    connectionToUse = currentConnection or connection
    print(connectionToUse)
    if connectionToUse is None:
        raise Exception("Initialize DB-connection before using it!")
    cursor = connectionToUse.cursor()
    try:
        cursor.execute(query)
        connectionToUse.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def create_tables(db_file):
    conn = None
    try:
        conn = connect(databasePath)
        execute_query(sql_create_dataset_info,conn)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def initConnection():
    global currentConnection
    try:
        currentConnection = connect(databasePath)
        execute_query(sql_create_dataset_info)
    except Error as e:
        print(e)

def closeConnection():
    global currentConnection
    if currentConnection:
        currentConnection.close()

