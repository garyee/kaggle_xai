from sqlite3 import connect, Error
from utils.kaggleEnums import KaggleEntityType, filePath, getIsCompetitionfromEntityType

databasePath = filePath+"kaggleSqlite.db"

currentConnection=None

sql_create_dataset_info = """ CREATE TABLE IF NOT EXISTS dataset_info (
                                    dataSetRef text NOT NULL PRIMARY KEY,
                                    is_competition BOOLEAN NOT NULL constraint enum_is_comp CHECK (is_competition IN (0, 1)) DEFAULT 0,
                                    type TEXT constraint enum_type CHECK( type IN ('Tabular','Image','Video','Text','Time Series','Bio_Chem','Sound','Misc') ) DEFAULT NULL,
                                    type_certainty INTEGER NULL constraint certainty_percentage CHECK (type_certainty>=0 and type_certainty<=100) DEFAULT 0,
                                    tab_interaction REAL NULL DEFAULT NULL,
                                    tab_features_total INTEGER NULL DEFAULT NULL,
                                    tab_cat_features INTEGER NULL DEFAULT NULL,
                                    tab_num_features INTEGER NULL DEFAULT NULL,
                                    tab_goal text constraint enum_tab_goal CHECK (tab_goal IN ('classification','regression','misc')) DEFAULT NULL
                                ); """

sql_create_kernel_info = """ CREATE TABLE IF NOT EXISTS kernel_info (
                                    kernelRef text NOT NULL PRIMARY KEY,
                                    dataSetRef text NOT NULL,
                                    hasBlackBoxModel BOOLEAN NOT NULL CHECK (hasBlackBoxModel IN (0, 1)) DEFAULT 0,
                                    hasGlassBoxModel BOOLEAN NOT NULL CHECK (hasBlackBoxModel IN (0, 1)) DEFAULT 0,
                                    Performance REAL NULL DEFAULT NULL,
                                    CONSTRAINT fk_dataSetRef
                                        FOREIGN KEY (dataSetRef)
                                        REFERENCES dataset_info (dataSetRef)
                                        ON DELETE CASCADE
                                ); """

sql_create_xai_methods = """ CREATE TABLE IF NOT EXISTS kernel_xai (
                                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                                    kernelRef text NOT NULL,
                                    hasBlackBoxModel BOOLEAN NOT NULL CHECK (hasBlackBoxModel IN (0, 1)) DEFAULT 0,
                                    CONSTRAINT fk_kernelRef
                                        FOREIGN KEY (kernelRef)
                                        REFERENCES kernel_info (kernelRef)
                                        ON DELETE CASCADE
                                ); """
sql_create_dataset_blacklist = """ CREATE TABLE IF NOT EXISTS dataset_blacklist (
                                    dataSetRef text NOT NULL PRIMARY KEY,
                                    is_competition BOOLEAN NOT NULL CHECK (is_competition IN (0, 1)) DEFAULT 0,
                                    reason text NULL DEFAULT NULL
                                ); """
# def insertOrUpdateKernelXAI(dataDict):


def shiftDataSetToBlackList(dataSetRef,entityType,reason):
    isCompetition=getIsCompetitionfromEntityType(entityType)
    createCommand="INSERT OR IGNORE INTO dataset_blacklist (dataSetRef,is_competition,reason) VALUES ('"+dataSetRef+"', '"+str(isCompetition)+"','"+reason+"');"
    execute_write_query(createCommand)
    deleteCommand="DELETE FROM dataset_info WHERE dataSetRef='"+dataSetRef+"';"
    execute_write_query(deleteCommand)




def insertDataBase(dataSetRef,is_competition):
    if(not isinstance(is_competition, int) or not isinstance(dataSetRef, str)):
        raise Exception("Error upon inserting a Database!")
    query="INSERT OR IGNORE INTO dataset_info (dataSetRef,is_competition) VALUES ('"+dataSetRef+"', '"+str(is_competition)+"');"
    execute_write_query(query)

def insertKernel(dataDict):
     sqlite_Insert_with_dict('kernel_info',dataDict)

def getAllEntityRefs():
    return execute_read_query("SELECT dataSetRef,is_competition FROM dataset_info")

def updateDataSetToDB(data,primaryKey='dataSetRef'):
    if primaryKey in data and len(data.keys())>1:
        sqlite_update_with_dict('dataset_info',primaryKey, data)

def sqlite_Insert_with_dict(table, data, connection=None):
    global currentConnection
    connectionToUse = currentConnection or connection
    if connectionToUse is None:
        raise Exception("Initialize DB-connection before using it!")
    try:
        cursor = currentConnection.cursor()

        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        query = "INSERT OR IGNORE INTO "+table+" ({}) VALUES ({})".format(columns, placeholders)
        cursor.execute(query, list(data.values()) )
    except Error as e:
        print(f"The error '{e}' occurred")

def sqlite_update_with_dict(table,primaryKeyName, data, connection=None):
    global currentConnection
    connectionToUse = currentConnection or connection
    if connectionToUse is None:
        raise Exception("Initialize DB-connection before using it!")
    try:
        cursor = currentConnection.cursor()
        primaryKeyValue=data.pop(primaryKeyName)

        query = f"UPDATE "+table+" SET " + ', '.join(
            "{}=?".format(k) for k in data.keys()) + f" WHERE "+primaryKeyName+"=?"
        # uncomment next line for debugging
        # print(query, list(data.values()) + [pkeyval])
        cursor.execute(query, list(data.values()) + [primaryKeyValue])
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_many(query,data,connection=None,silent=True):
    global currentConnection
    connectionToUse = currentConnection or connection
    if connectionToUse is None:
        raise Exception("Initialize DB-connection before using it!")
    cursor = currentConnection.cursor()
    try:
        cursor.executemany(query,data)
        currentConnection.commit()
        if silent==False:
            print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_write_query(query,connection=None,silent=True):
    global currentConnection
    connectionToUse = currentConnection or connection
    if connectionToUse is None:
        raise Exception("Initialize DB-connection before using it!")
    cursor = connectionToUse.cursor()
    try:
        cursor.execute(query)
        connectionToUse.commit()
        if silent==False:
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
        if currentConnection==None :
            currentConnection = connect(databasePath)
        execute_write_query(sql_create_dataset_info)
        execute_write_query(sql_create_kernel_info)
        execute_write_query(sql_create_xai_methods)
        execute_write_query(sql_create_dataset_blacklist)
    except Error as e:
        print(e)

def closeConnection():
    global currentConnection
    if currentConnection:
        currentConnection.close()
        currentConnection=None

