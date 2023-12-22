from GrinApp import app
from flask import render_template, request, jsonify
import GrinApp.SQLTool as sqlTool
from datetime import date
from GrinApp.Login import login_required
from GrinApp.service import seperateTables
today = date.today()
date = today.strftime("%m/%d/%Y")



#took AdditionalName out of columns
@app.route("/customers/")
@login_required
def customers():
    options = optionData()
    return render_template('addCustomers.html', rendering=True, customerInfo="", inactive="false", phoneTypes=options[5], tNumKnives=options[4], cutterHead=options[3], 
        knifeMaterial=options[2], backClearance=options[1], hookAngles=options[0], machineTypes=options[6], contacts="", comments="", technicalInfo="")

@app.route("/customers/newcustomer", methods=["POST"])
@login_required
def newCustomer():
    data=request.get_json()
    sqlTool.QueryBuilder.insertIntoTable('customers', 'CustomerNumber, CustomerName, Address1, Address2, City, State, Zip, Zip4, FileName, AdditionalNames, Inactive, TemplateCustomer, KnifeCustomer, Roughgrindcustomer', f"{int(data['custNumber'])}, '{data['custName']}', '{data['address1']}', '{data['address2']}', '{data['city']}', '{data['state']}', {int(data['zip'])}, '{data['zip4']}', '{data['fileName']}', '{data['additionalInfo']}', 'false', 'false', 'false', 'false'")
    return data

@app.route("/customers/updatecustomer", methods=["POST"])
@login_required
def updateCustomer():
    data=request.get_json()
    print("Update fired!")
    return data

@app.route("/addCustomers/loaded", methods=["GET"])
@login_required
def addCustomers():
    name = request.args.get('custName')
    customerInfo = sqlTool.QueryBuilder.readWhereFromTable('customers', "*", f'CustomerName= "{name}"')
    inactive = customerInfo[0]['Inactive'].lower()
    contacts = sqlTool.QueryBuilder.readWhereFromTable('customercontactlist', "*", f'CustomerID= {customerInfo[0]["CustomerNumber"]}')
    comments = sqlTool.QueryBuilder.readWhereFromTable('customercomments', "*", f'CustomerID= {customerInfo[0]["CustomerID"] }')
    technicalInfo = sqlTool.QueryBuilder.readWhereFromTable('technicalinfo', "*", f'CustomerID= {customerInfo[0]["CustomerID"]}')
    print(technicalInfo)
    options = optionData()
    print(options[2])
    return render_template('addCustomers.html', rendering=True, customerInfo=customerInfo[0], inactive=inactive, phoneTypes=options[5], tNumKnives=options[4], cutterHead=options[3], 
        knifeMaterial=options[2], backClearance=options[1], hookAngles=options[0], machineTypes=options[6], contacts=contacts, comments=comments, technicalInfo=technicalInfo[0])

def optionData():
    options = sqlTool.QueryBuilder.customQuery(f'''
        select HookAngleID, HookAngleDesc, NULL AS BackClearanceID, NULL AS BackClearanceDesc, NULL AS CutterheadID, 
        NULL AS CutterheadDesc, NULL AS KnifeMaterialID, NULL AS KnifeMaterialDesc,NULL AS NumKnivesPerHeadID, 
        NULL AS NumKnivesPerHeadDesc, NULL AS PhoneTypeID, NULL AS Description from hookangles
        union
        select NULL AS HookAngleID, NULL AS HookAngleDesc, BackClearanceID,BackClearanceDesc, NULL AS CutterheadID, 
        NULL AS CutterheadDesc, NULL AS KnifeMaterialID, NULL AS KnifeMaterialDesc, NULL AS NumKnivesPerHeadID, 
        NULL AS NumKnivesPerHeadDesc, NULL AS PhoneTypeID, NULL AS Description from backclearance
        union
        select NULL AS HookAngleID, NULL AS HookAngleDesc, NULL AS BackClearanceID, NULL AS BackClearanceDesc, CutterheadID, 
        CutterheadDesc, NULL AS KnifeMaterialID, NULL AS KnifeMaterialDesc, NULL AS NumKnivesPerHeadID, NULL AS NumKnivesPerHeadDesc, NULL AS PhoneTypeID, 
        NULL AS Description from cutterheads
        union
        select NULL AS HookAngleID, NULL AS HookAngleDesc, NULL AS BackClearanceID, NULL AS BackClearanceDesc, NULL AS CutterheadID, 
        NULL AS CutterheadDesc, KnifeMaterialID, KnifeMaterialDesc, NULL AS NumKnivesPerHeadID, NULL AS NumKnivesPerHeadDesc, NULL AS PhoneTypeID, NULL AS Description
        from knifematerials
        union
        select NULL AS HookAngleID, NULL AS HookAngleDesc, NULL AS BackClearanceID, NULL AS BackClearanceDesc, NULL AS CutterheadID, 
        NULL AS CutterheadDesc, NULL AS KnifeMaterialID, NULL AS KnifeMaterialDesc, NumKnivesPerHeadID, NumKnivesPerHeadDesc, NULL AS PhoneTypeID, NULL AS Description
        from numknivesperhead
        union
        select NULL AS HookAngleID, NULL AS HookAngleDesc, NULL AS BackClearanceID, NULL AS BackClearanceDesc, NULL AS CutterheadID, 
        NULL AS CutterheadDesc, NULL AS KnifeMaterialID, NULL AS KnifeMaterialDesc, NULL AS NumKnivesPerHeadID, NULL AS NumKnivesPerHeadDesc, PhoneTypeID, Description
        from phonetypes
        ''')
    machineTypes = sqlTool.QueryBuilder.readFromTable("machinetypes", "*")
    hookAngles = seperateTables("HookAngle", options)
    backClearance = seperateTables("BackClearance", options)
    knifeMaterial = seperateTables("KnifeMaterial", options)
    cutterHead = seperateTables("Cutterhead", options)
    tNumKnives = seperateTables("NumKnivesPerHead", options)
    phoneTypes = seperateTables("PhoneType", options)

    return [hookAngles, backClearance, knifeMaterial, cutterHead, tNumKnives, phoneTypes, machineTypes]

@app.route('/addContacts', methods=['POST'])
@login_required
def addContacts():
    data = request.get_json()
    if (data[0] != "delete"):
        insertID = infoInserts('customercontactlist',data[1])
        data[1]['insertID'] = insertID
        return data[1]
    else:
        sqlTool.QueryBuilder.deleteFromTable('customercontactlist', f"CustomerContactListID = {data[1]}")
        return jsonify({'message':'Delete successful'}), 200

@app.route('/addComments', methods=['POST'])
@login_required
def addComments():
    data= request.get_json()
    print(data)
    if (data[0] != "delete"):
        insertID = infoInserts('customercomments',data[1])
        data[1]['insertID'] = insertID
        return data[1]
    else:
        sqlTool.QueryBuilder.deleteFromTable('customercomments', f'CustomerID = {data[1][0]} and Comment = "{data[1][1]}"')
        return jsonify({'message':'Delete successful'}), 200

@app.route('/updateTechInfo', methods=['POST'])
@login_required
def updateTechInfo():
    data=request.get_json()
    print(data)
    return data

def infoInserts(table, data):
    if (table == "customercontactlist"):
        columns = 'CustomerID, FirstName, LastName, Email, PhoneNumber, PhoneTypeID'
        dataString = f'{data["CustomerNumber"]}, "{data["firstName"]}", "{data["lastName"]}", "{data["email"]}", "{data["phoneNumber"]}", {data["phoneType"]}'
    if (table =="customercomments"):
        columns='CustomerID, Date, Comment'
        dataString=f'{data["CustomerNumber"]}, "{data["date"]}", "{data["comment"]}"'
    insertID = sqlTool.QueryBuilder.insertIntoTable(table, columns, dataString)
    return insertID