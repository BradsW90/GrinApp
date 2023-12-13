from GrinApp import app
from flask import render_template, request, jsonify, url_for, redirect, session
import GrinApp.SQLTool as sqlTool
from datetime import date
from GrinApp.Login import login_required
today = date.today()
date = today.strftime("%m/%d/%Y")


#serves data for the auto suggest in searchbar of addServicePage and addCustomersPage
@app.route("/preAddService/")
@login_required
def preAddService():
    customerNames = sqlTool.QueryBuilder.readFromTable("customers", "CustomerNumber, CustomerName")
    return jsonify(data=customerNames)


#renders add service page
@app.route("/addService/", methods=["GET"])
@login_required
def addService():
    return render_template('addService.html', tips='', chosenName='',user=False, rendering=True)


#populates customer and page data off of customer search
#handles delete of full services
@app.route("/addService/loaded/", methods=["GET", "POST"])
@login_required
def addServiceEdit():
    if request.method == "POST":
        data = request.get_json()
        if (data['data'] == "serviceDelete"):
            detailsToDelete = sqlTool.QueryBuilder.readWhereFromTable('customerservicedetails', 'CustomerServiceDetailID', f'CustomerServiceID = {data["id"]}')
            if (len(detailsToDelete) != 0):
                for details in detailsToDelete:
                    sqlTool.QueryBuilder.deleteFromTable("customerservicedetails", f"CustomerServiceDetailID = {details['CustomerServiceDetailID']}")
            sqlTool.QueryBuilder.deleteFromTable("customerservices", f"CustomerServiceID = {data['id']}")
            return jsonify({'message': 'Delete successful'})
        else:

            sqlTool.QueryBuilder.deleteFromTable('customerservicedetails', f"CustomerServiceDetailID = {data['id']}")
            return jsonify({'message': 'Delete successful'})
    else:
        name = request.args.get('custName')
        userID = session.get('user_id')
        #User name query
        user = sqlTool.QueryBuilder.customQuery(f"select FirstName, LastName from users where UserID = {userID}")
        # Customer Info Table
        customerInfo = sqlTool.QueryBuilder.readWhereFromTable("customers", "CustomerNumber, Tips", f'CustomerName = "{name}"')
        if (len(customerInfo) == 0):
            return redirect(url_for('addService'));
        #Gets data to populate ServiceList section of /addService/ page
        previousServiceList = sqlTool.QueryBuilder.customQuery(f"""
            select CustomerServiceID, date, ShipDate, NumTemplates, orderplacedbyid from customerservices
            join customers on customers.CustomerID = customerservices.CustomerID
            where CustomerName = '{name}'
            order by CustomerServiceID DESC
            """)
        # Comments table
        data = sqlTool.QueryBuilder.customQuery(f"""
            select customercomments.Date as Date, customercomments.Comment as comments from customercomments 
            join customers on customers.CustomerID = customercomments.CustomerID 
            where customers.CustomerNumber = '{customerInfo[0]['CustomerNumber']}' ORDER BY 'Date' DESC;
            """)
        #Customers Technical Info Data
        technicalInfo = sqlTool.QueryBuilder.customQuery(f"""
            select hookangles.HookAngleID, hookangles.HookAngleDesc, backclearance.BackClearanceID, backclearance.BackClearanceDesc, 
            knifematerials.KnifeMaterialID, knifematerials.KnifeMaterialDesc, cutterheads.CutterheadID, cutterheads.CutterheadDesc, 
            numknivesperhead.NumKnivesPerHeadID, numknivesperhead.NumKnivesPerHeadDesc from technicalinfo
            join hookangles on hookangles.HookAngleID = technicalinfo.HookAngleID
            join backclearance on backclearance.BackClearanceID = technicalinfo.BackClearanceID
            join knifematerials on knifematerials.KnifeMaterialID = technicalinfo.KnifeMaterialID
            join cutterheads on cutterheads.CutterHeadID = technicalinfo.CutterHeadID
            join numknivesperhead on numknivesperhead.NumKnivesPerHeadID = technicalinfo.NumKnivesPerHeadID
            join customers on technicalinfo.CustomerID = customers.CustomerID
            where customers.CustomerNumber = '{customerInfo[0]['CustomerNumber']}';
            """)
        #Technical Info Table
        technicalInfoSelections = sqlTool.QueryBuilder.customQuery(f"""
            select HookAngleID, HookAngleDesc, NULL AS BackClearanceID, NULL AS BackClearanceDesc, NULL AS CutterheadID, 
            NULL AS CutterheadDesc, NULL AS KnifeMaterialID, NULL AS KnifeMaterialDesc,NULL AS NumKnivesPerHeadID, 
            NULL AS NumKnivesPerHeadDesc, NULL AS HeadPositionID, NULL AS HeadPositionDesc from hookangles
            union
            select NULL AS HookAngleID, NULL AS HookAngleDesc, BackClearanceID,BackClearanceDesc, NULL AS CutterheadID, 
            NULL AS CutterheadDesc, NULL AS KnifeMaterialID, NULL AS KnifeMaterialDesc,NULL AS NumKnivesPerHeadID, 
            NULL AS NumKnivesPerHeadDesc, NULL AS HeadPositionID, NULL AS HeadPositionDesc from backclearance
            union
            select NULL AS HookAngleID, NULL AS HookAngleDesc, NULL AS BackClearanceID, NULL AS BackClearanceDesc, CutterheadID, 
            CutterheadDesc, NULL AS KnifeMaterialID, NULL AS KnifeMaterialDesc, NULL AS NumKnivesPerHeadID, NULL AS NumKnivesPerHeadDesc, NULL AS HeadPositionID, 
            NULL AS HeadPositionDesc from cutterheads
            union
            select NULL AS HookAngleID, NULL AS HookAngleDesc, NULL AS BackClearanceID, NULL AS BackClearanceDesc, NULL AS CutterheadID, 
            NULL AS CutterheadDesc, KnifeMaterialID, KnifeMaterialDesc, NULL AS NumKnivesPerHeadID, NULL AS NumKnivesPerHeadDesc, NULL AS HeadPositionID, NULL AS HeadPositionDesc
            from knifematerials
            union
            select NULL AS HookAngleID, NULL AS HookAngleDesc, NULL AS BackClearanceID, NULL AS BackClearanceDesc, NULL AS CutterheadID, 
            NULL AS CutterheadDesc, NULL AS KnifeMaterialID, NULL AS KnifeMaterialDesc,NumKnivesPerHeadID, NumKnivesPerHeadDesc, NULL AS HeadPositionID, NULL AS HeadPositionDesc
            from numknivesperhead
            union
            select NULL AS HookAngleID, NULL AS HookAngleDesc, NULL AS BackClearanceID, NULL AS BackClearanceDesc, NULL AS CutterheadID, 
            NULL AS CutterheadDesc, NULL AS KnifeMaterialID, NULL AS KnifeMaterialDesc, NULL AS NumKnivesPerHeadID, NULL AS NumKnivesPerHeadDesc, HeadPositionID, HeadPositionDesc
            from headpositions
            """)
        hookAngles = seperateTables("HookAngle", technicalInfoSelections)
        backClearance = seperateTables("BackClearance", technicalInfoSelections)
        knifeMaterial = seperateTables("KnifeMaterial", technicalInfoSelections)
        cutterHead = seperateTables("Cutterhead", technicalInfoSelections)
        tNumKnives = seperateTables("NumKnivesPerHead", technicalInfoSelections)
        headPositions = seperateTables("HeadPosition", technicalInfoSelections)
        return render_template('addService.html', tips=customerInfo[0]['Tips'], customerNames=name, chosenName=name, customerNumber=customerInfo[0]['CustomerNumber'], data=data, 
            hookAngles=hookAngles, headPositions=headPositions, backClearance=backClearance, knifeMaterial=knifeMaterial, cutterHead=cutterHead, tNumKnives=tNumKnives, 
            previousServiceList=previousServiceList, technicalInfo=technicalInfo[0], user=user[0], rendering=True, nonSearch=True)


#Gets info based on id for print page
#Posts new service based on searched customer and inputs on form
@app.route("/addService/loaded/print/", methods=["POST"])
@app.route("/addService/loaded/print/<int:id>", methods=["GET"])
@login_required
def printData (id = None):
    if (request.method == "POST"):
        data = request.get_json()
        nonServiceDetail = data[-12:]
        nonServiceDetail[4] = session.get('user_id')
        print(nonServiceDetail[4])
        CustID = sqlTool.QueryBuilder.readWhereFromTable("customers", "CustomerID", f"CustomerNumber = {nonServiceDetail[11]}")
        nonServiceDetail[11] = CustID[0]['CustomerID']
        for index, item in enumerate(nonServiceDetail):
            if (index >= 5 and index <= 10):
                nonServiceDetail[index] = int(item)
        nonServiceDetail = nonServiceDetail + [5,9,4]
        customerService = sqlTool.QueryBuilder.insertIntoTable('customerservices', 'CustomerID, date, ShipDate, ShipperID, InspectorID, NumTemplates, KnifeMaterialID, CutterHeadID, HookAngleID, BackClearanceID, TemplateDestID, NumKnivesPerHeadID, orderplacedbyid, OrderTakenByID, comments', f'"{nonServiceDetail[11]}", "{nonServiceDetail[0]}", "{nonServiceDetail[1]}", {nonServiceDetail[12]}, {nonServiceDetail[13]}, {nonServiceDetail[5]}, {nonServiceDetail[6]}, {nonServiceDetail[7]}, {nonServiceDetail[8]}, {nonServiceDetail[9]}, {nonServiceDetail[14]}, {nonServiceDetail[10]}, "{nonServiceDetail[3]}", {nonServiceDetail[4]}, "{nonServiceDetail[2]}"')
        insertServiceDetails(customerService, data)
        return jsonify({'message': 'Data inserted successfully', "inserted_id": customerService}), 200
    else:
        service = sqlTool.QueryBuilder.customQuery(f"""
            select customers.CustomerName, date, ShipDate, NumTemplates, comments, knifematerials.KnifeMaterialDesc, cutterheads.CutterheadDesc, hookangles.HookAngleDesc, backclearance.BackClearanceDesc, 
            numknivesperhead.NumKnivesPerHeadDesc, orderplacedbyid, users.FirstName, users.LastName from customerservices
            join knifematerials on knifematerials.KnifeMaterialID = customerservices.KnifeMaterialID
            join cutterheads on cutterheads.CutterheadID = customerservices.CutterheadID
            join hookangles on hookangles.HookAngleID = customerservices.HookAngleID
            join backclearance on backclearance.BackClearanceID = customerservices.BackClearanceID
            join numknivesperhead on numknivesperhead.NumKnivesPerHeadID = customerservices.NumKnivesPerHeadID
            join users on users.UserID = customerservices.OrderTakenByID
            join customers on customers.CustomerID = customerservices.CustomerID
            where CustomerServiceID = {id}
            """)
        details = sqlTool.QueryBuilder.customQuery(f"""
            select NumKnives, Width, Length, HeadPositions.HeadPositionDesc, Quantity, CustomTemplateDesc, Waterjet, Note from customerservicedetails
            join headpositions on headpositions.HeadPositionID = customerservicedetails.HeadPositionID
            where CustomerServiceID = {id}
            """)
        return render_template('serviceTicket.html', service=service[0], details=details, rendering=False)


#Gets info based on service clicked
#Posts service details to current service clicked
@app.route("/addService/oldService/<int:id>", methods=["GET", "POST"])
@login_required
def oldService(id):
    if (request.method == "POST"):
        data = request.get_json()
        if (len(data) > 11):
            insertServiceDetails(id, data)
        return jsonify({'message': 'Through POST', 'serviceID': id})
    else:
        serviceQuery = sqlTool.QueryBuilder.customQuery(f"""
            select date, ShipDate, NumTemplates, knifematerials.KnifeMaterialDesc, cutterheads.CutterheadDesc, hookangles.HookAngleDesc, 
            backclearance.BackClearanceDesc, numknivesperhead.NumKnivesPerHeadDesc, orderplacedbyid, users.FirstName, users.LastName, customerservicedetails.
            CustomerServiceID, customerservicedetails.NumKnives, customerservicedetails.Width, customerservicedetails.Length, headpositions.HeadPositionDesc, 
            customerservicedetails.Quantity, customerservicedetails.CustomTemplateDesc, customerservicedetails.Waterjet, customerservicedetails.Note, 
            customerservicedetails.CustomerServiceDetailID, knifematerials.KnifeMaterialID, cutterheads.CutterheadID, hookangles.HookAngleID, 
            backclearance.BackClearanceID, numknivesperhead.NumKnivesPerHeadID
            from customerservices
            join knifematerials on knifematerials.KnifeMaterialID = customerservices.KnifeMaterialID
            join cutterheads on cutterheads.CutterheadID = customerservices.CutterheadID 
            join hookangles on hookangles.HookAngleID = customerservices.HookAngleID
            join backclearance on backclearance.BackClearanceID = customerservices.BackClearanceID
            join numknivesperhead on numknivesperhead.NumKnivesPerHeadID = customerservices.NumKnivesPerHeadID
            join users on users.UserID = customerservices.OrderTakenByID
            join customerservicedetails on customerservicedetails.CustomerServiceID = customerservices.CustomerServiceID
            join headpositions on headpositions.HeadPositionID = customerservicedetails.HeadPositionID
            where customerservices.CustomerServiceID = {id}
            """)
        return jsonify(serviceQuery=serviceQuery)


#Used to take multi 2 column queries and seperate them into different variables
def seperateTables (tableName, segment):
    newList = []
    for data in segment:
        newObj = {"id": 0, "Desc": ""}
        for key, value in data.items():
            if (tableName in key and value != None or "Description" in key and value != None and tableName == "PhoneType"):
                if ("ID" in key):
                    newObj['id'] = value
                elif ("Desc" in key):
                    newObj['Desc'] = value
        if (newObj['Desc'] != ""):
            newList.append(newObj)
    return newList

#Inserts serviceDetails based on passed in info
def insertServiceDetails (customerService, data):
    for index, item in enumerate(data):
            if (index < len(data) - 12):
                sqlTool.QueryBuilder.insertIntoTable('customerservicedetails', 'CustomerServiceID, NumKnives, Width, Length, HeadPositionID, Quantity, CustomTemplateDesc, Waterjet, Note', f"{customerService}, {int(item['data'][3])}, '{item['data'][4]}', '{item['data'][5]}', {int(item['data'][6])}, {float(item['data'][0])}, '{item['data'][1]}', '{item['data'][7]}', '{item['data'][2]}'")