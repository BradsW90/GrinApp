document.addEventListener("DOMContentLoaded", function() {
	//all input fields
    const serviceInputs = document.getElementsByClassName('newService');
    //current date field
    const dateInput = document.getElementById('todayDate');
    //New Service Form button
    const addServiceBtn = document.getElementById('addServiceBtn');
    //table row to render the add service to
    const renNewService = document.querySelectorAll('.renNewService');
    //List of customers previous services
    const serviceList = document.getElementById('serviceList');
    //Reference to print button
    const printBtn = document.getElementById('printBtn');
    //Gets element containing customers ID
    const custID = document.getElementById('customer');
    //Gets searchbar element
    const searchBar = document.getElementById('customerNameSelect');
    //Gets clear button element
    const clearBtn = document.getElementById('clearBtn');
    //array for database commit
    let serviceDetail = [];
    //sets unique ids for objects
    let id = 0;
    //grabs todays date
    let today = new Date().toISOString().split('T')[0];
    //prefills todays date field
    dateInput.value = today;
    //Sets up a variable to toggle if the print button functionality
    let pass = new toUpdate(false, "");
    //List of object Key names to access and assign values to elements in correct order
    let serviceLabels = ["Quantity", "CustomTemplateDesc", "Note", "NumKnives", "Width", "Length", "HeadPositionDesc", "Waterjet", "NumTemplates", "KnifeMaterialID", "CutterheadID", "HookAngleID", "BackClearanceID", "NumKnivesPerHeadID"];


    //Takes information entered into new service and renders it into New Service table while setting the same data up in background for future insert statement
    //Sets up delete button with ability to remove itself from table and background data array
    addServiceBtn.addEventListener('click', function() {
        id += 1;        
    	let newRow = document.createElement('tr');
    	let deleteCell = document.createElement('td');
    	let deleteBtn = document.createElement('button');
    	deleteBtn.innerText = "Delete";
        deleteBtn.setAttribute("data-id", id);

        deleteBtn.addEventListener("click", function (e) {
            e.preventDefault();
            const rowID = e.target.getAttribute("data-id");
            for (j=0; j<serviceDetail.length; j++) {
                if (serviceDetail[j].id.toString() === rowID) {
                    serviceDetail.splice(j,1);
                }
            }
            e.target.parentNode.parentNode.remove();
        });
    	deleteCell.appendChild(deleteBtn);
    	newRow.appendChild(deleteCell);
        let newRowData = new rowData(id, [])
    	for (i=0; i <serviceInputs.length; i++) {
            if (i <= 7) {
                let newData = document.createElement('td');
                if (i===7) {
                    newData.innerText = serviceInputs[i].checked;
                    newRow.appendChild(newData);
                    newRowData.data.push(serviceInputs[i].checked);
                } else {
                    if (serviceInputs[i].value === "") {
                        alert("One  or more fields are Blank!");
                        return;
                    }
                    newData.innerText = serviceInputs[i].value;
                    newRow.appendChild(newData);
                    newRowData.data.push(serviceInputs[i].value);
                }    
            }
    		if (serviceInputs[i].type === "checkbox") {
    			serviceInputs[i].checked = false;
    		}else if (i<=7) {
    			serviceInputs[i].value = "";
    		}
    	}
    	renNewService[0].appendChild(newRow);
        serviceDetail.push(newRowData);
    });


    //Sets onClick handling on service table body
    //On Delete click confirms then deletes service and subsequent servicedetails then refreshes screen
    serviceList.addEventListener('click', function (e) {
        if (e.target.tagName.toLowerCase() === "button") {
            //console.log(e.target.getAttribute("data-id"));
            toDelete = window.confirm("What you have chosen to delete is apart of the database, are you sure you want to delete?");
            if (toDelete) {
                forDelete = new rowData(e.target.getAttribute("data-id"), "serviceDelete")
                fetch('/addService/loaded', {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(forDelete)
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response not ok');
                    }
                    return response.json()
                })
                .then(data => {
                    window.location.reload();
                })
            }
        } else {
            customerServiceID = e.target.parentNode.getAttribute('data-id');
            pass.update = true;
            pass.serviceID = customerServiceID;
            newService = document.querySelectorAll('.renNewService');
            while (newService[0].firstChild) {
                newService[0].removeChild(newService[0].firstChild);
            }
            $.ajax({
                url: `/addService/oldService/${e.target.parentNode.getAttribute('data-id')}`,
                method: 'GET',
                success: function (response) {
                    data2 = response.serviceQuery
                    for (i=0; i<data2.length; i++) {
                        newRow = document.createElement('tr');
                        let deleteCell = document.createElement('td');
                        let deleteBtn = document.createElement('button');
                        deleteBtn.innerText = "Delete";
                        deleteBtn.setAttribute("data-id", data2[i].CustomerServiceDetailID);

                        deleteBtn.addEventListener("click", function (e) {
                            e.preventDefault();
                            toDelete = window.confirm("What you have chosen to delete is apart of the database, are you sure you want to delete?");
                            if (toDelete) {
                                forDelete = new rowData(e.target.getAttribute("data-id"), "detailDelete")
                                fetch('/addService/loaded', {
                                    method: "POST",
                                    headers: {
                                        'Content-Type': 'application/json'
                                    },
                                    body: JSON.stringify(forDelete)
                                })
                                .then(response => {
                                    if (!response.ok) {
                                        throw new Error('Network response not ok');
                                    }
                                })
                            }
                            e.target.parentNode.parentNode.remove();
                        });
                        deleteCell.appendChild(deleteBtn);
                        newRow.appendChild(deleteCell);
                        for (j=0; j<serviceLabels.length-6; j++) {
                            let cell = document.createElement('td');
                            cell.innerText = data2[i][serviceLabels[j]];
                            newRow.appendChild(cell);
                        }
                        for (h=12; h<serviceInputs.length; h++) {
                            serviceInputs[h].value = data2[i][serviceLabels[h-4]]
                        }
                        renNewService[0].appendChild(newRow);
                    }
                },
                error: function (error) {
                    console.log('Error: ', error);
                }
            });
        }
    })


    //Handles new CustomerService insert or just servicedetail insert, then opens print page and refeshes app
    printBtn.addEventListener('click', function() {
        if (searchBar.value === "") {
            return;
        }
        if (serviceDetail.length === 0 && !pass.update) {
            alert("No New Service Objects!");
            return;
        }
        if (pass.update) {
            pass.update = false;
            appendData();
            fetch(`/addService/oldService/${pass.serviceID}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(serviceDetail)
            })
            .then(response => {
                if(!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json()
            })
            .then(data => {
                window.open(`http://127.0.0.1:5000/addService/loaded/print/${data.serviceID}`)
                window.location.reload();
            })
        } else {
            appendData();
            fetch('/addService/loaded/print/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(serviceDetail)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response not ok');
                }
                return response.json();
            })
            .then(data => {
                window.open(`http://127.0.0.1:5000/addService/loaded/print/${data.inserted_id}`)
                window.location.reload();
            })
            .catch(error => {
                console.error('Error', error);
            });
        }
    });

    //Clears form
    clearBtn.addEventListener("click", function() {
        window.location.reload();
    })


    //used to prepare data for print methods
    function appendData() {
        let form = document.getElementsByClassName('newService');
        for(i=8; i<form.length; i++) {
            serviceDetail.push(form[i].value);
        }
        serviceDetail.push(parseInt(custID.getAttribute('data-cid')));
    };

});


//Used for data structure on inserts and for accessing data beforehand
class rowData {
    constructor(id, data) {
        this.id = id;
        this.data = data;
    }
}


//used to setup print function
class toUpdate {
    constructor(update, serviceID) {
        this.update = update;
        this.serviceID = serviceID;
    }
}