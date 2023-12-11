from GrinApp.connection import DBConnection

class QueryBuilder:
    
    def columnFinder(tableName):
        query = 'select * FROM %s;' % tableName
        queryResults = DBConnection.queryDescription(query)
        return queryResults
    
    def readFromTable(tableName, columnNames):

        query = 'select %s from %s;' % (columnNames, tableName)
        queryResults = DBConnection.queryAll(query)
        return queryResults
    
    def customQuery(query):
        queryResults = DBConnection.queryAll(query)
        return queryResults

    def insertIntoTable(tableName, columnNames, columnValues):
        try:
            query = 'Insert into %s (%s) VALUES (%s);' % (tableName, columnNames, columnValues)
            newID = DBConnection.queryCommit(query)
            print("Query inserted into table")
            return newID
        except Exception as error:
            print(f"Query did not insert into table: {error}")

    def alterTableADD(tableName, columnName, dataType):
        try:
            query = "Alter Table %s ADD %s %s;" % (tableName, columnName, dataType)
            DBConnection.queryCommit(query)
            print("Table was altered")
        except:
            print("Table was not altered")

    def alterTableDROP(tableName, columnName):
        try:
            query = "Alter Table %s DROP COLUMN %s;" % (tableName, columnName)
            DBConnection.queryCommit(query)
            print("Table was altered")
        except:
            print("Table was not altered")

    def alterTableMODIFY(tableName, columnName, dataType):
        try:
            query = "Alter Table %s MODIFY Column %s %s;" % (tableName, columnName, dataType)
            DBConnection.queryCommit(query)
            print("Table was altered")
        except:
            print("Table was not altered")

    def updateTable(tableName, columnEqualValue, condition):
        try:
            query = "Update %s set %s WHERE %s;" % (tableName, columnEqualValue, condition)
            DBConnection.queryCommit(query)
            print("Entry was updated")
        except:
            print("Entry was not updated")
            
    def filterTable(tableName, columnNames, filterColumns):
        query = 'select %s from %s ORDER BY %s;' % (columnNames, tableName, filterColumns)
        queryResults = DBConnection.queryAll(query)
        return queryResults

    def deleteFromTable(tableName, condition):
        try:
            query = "DELETE from %s WHERE %s;" % (tableName, condition)
            DBConnection.queryCommit(query)
            print("Entry was deleted")
        except:
            print("Entry was not deleted")

    def readWhereFromTable(tableName, columnNames, condition):
        query = 'select %s from %s where %s;' % (columnNames, tableName, condition)
        queryResults = DBConnection.queryAll(query)
        return queryResults

    def singleReadWhere(tableName, columnNames, condition):
        query = 'SELECT %s FROM %s WHERE %s;' % (columnNames, tableName, condition)
        queryResults = DBConnection.queryOne(query)
        return queryResults