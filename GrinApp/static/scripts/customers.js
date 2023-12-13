document.addEventListener('DOMContentLoaded', function(){
	const tabs = document.getElementById('tabs');
	const title = document.getElementById('tabTitle');
	const additionalInfo = document.getElementById('additionalInfo');
	const customerBTN = document.getElementById('customerBTN');
	const tabTable = document.getElementsByClassName('tabTable');
	const contactTable = document.getElementById('contactTable');
	const commentTable = document.getElementById('commentTable');
	const techInfoTable = document.getElementById('techInfoTable');
	const equipmentTable = document.getElementById('equipmentTable');
	const customerSearch = document.getElementById('customerSearch');
	const customerMessage = document.getElementsByClassName('message');
	const tabMessage = document.getElementsByClassName('tabMessage');
	const contactHeaders = document.getElementById('contactHeaders');

	var newCustomer = true;
	const contactGroup = ['1%','19.8%', '19.8%','19.8%','19.8%','19.8%'];
	const commentGroup = ['1%', '49.5%', '49.5%'];
	const techInfoGroup = ['1%', '14.14%','14.14%','14.14%','14.14%','14.14%'];
	const equipmentGroup = ['1%', '33%','33%','33%'];

	//presets page functionality based on url address
	let location = window.location.href.split("/");
	if (location[3] === "addCustomers") {
		newCustomer = false;
	}

	//Gives the tabs the ability to be highlighted and to render the correct form based on tab
	tabs.addEventListener('click', function(e) {
		var active = tabs.querySelector('.th-shaded');
		if (e.target.innerText != active.innerText && e.target.innerText.length != 42) {
			active.classList.remove('th-shaded');
			e.target.classList.add('th-shaded');
			title.textContent = e.target.innerText;
		};
		switch(e.target.innerText) {
		case "Contacts":
			additionalInfo.setAttribute("data-info", "contacts");
			correctRender(contactTable, contactGroup);
			break;

		case "Comments":
			additionalInfo.setAttribute("data-info", "comments");
			correctRender(commentTable, commentGroup);
			break;

		case "Technical Info":
			additionalInfo.setAttribute("data-info", "techInfo");
			correctRender(techInfoTable, techInfoGroup);
			break;

		case "Equipment":
			additionalInfo.setAttribute("data-info", "equipment");
			correctRender(equipmentTable, equipmentGroup);

		default:
			break;
		}
	});

	// Customer form save functionality
	customerBTN.addEventListener('click', function() {
		resetMessage();
		if (newCustomer) {
			let newCustomerData = getCustomerForm('customerForm', 'customer', customerMessage);
			newCustomer = false;
			sendData('/customers/newcustomer', newCustomerData);
        } else {
        	let newCustomerData = getCustomerForm('customerForm', 'customer', customerMessage);
        	sendData('/customers/updatecustomer', newCustomerData);
        };
	});

	//Tab form save functionality
	additionalInfo.addEventListener('click', function () {
		resetMessage()
		for (j=0; j<tabTable.length; j++) {
			if (!tabTable[j].hasAttribute('hidden')) {
				switch(document.getElementById('tabTitle').innerText) {
				case "CONTACTS":
					if (!newCustomer) {
						let newData = getCustomerForm('contactForm', 'contacts', tabMessage);
						newData[0].CustomerNumber = document.getElementById('custNumber').value;
						console.log(newData);
						sendData('/addContacts', newData);
					}
				}
			}
		}
	})

	//function to handle tab form rendering
	function correctRender(element, spacing) {
		var colGroup = document.getElementById('tabGroup');
		clearContainer(colGroup);
		for (k=0; k<spacing.length; k++) {
			var col = document.createElement('col');
			col.setAttribute('span', '1');
			col.setAttribute('style', `width: ${spacing[k]}`)
			colGroup.appendChild(col);
		}
		for (l=0; l<tabTable.length; l++) {
			if (!tabTable[l].hasAttribute('hidden')) {
				tabTable[l].setAttribute('hidden', true);
			}
		}
		element.removeAttribute('hidden');
	};

	//function to clear a parent element
	function clearContainer(element) {
		while (element.firstChild) {
			element.removeChild(element.firstChild);
		};
	};

	//function to grab form data and performs required checks
	function getCustomerForm(className, id, message) {
		var formData = document.getElementsByClassName(className);
		var toObject = [];
		var notCorrect = false;
		let newCustomerData;
		for (i=0; i<formData.length;i++) {
			toObject.push(formData[i].value);
		}
		switch(id) {
		case "customer":
			newCustomerData = new CustomerData(toObject);
			break;

		case "contacts":
			newCustomerData = new ContactData(toObject);
			break;
		}
			for (i=0; i<formData.length; i++) {
				if (formData[i].hasAttribute('required') && formData[i].value.trim() === "") {
					formData[i].style.border = '1px solid red';
					notCorrect = true;
				} else {
					formData[i].style.border = "";
				}
			}
			if (notCorrect) {
				return [newCustomerData, true, id];
			} else {
				for (j=0; j<message.length; j++) {
					if (!message[j].hasAttribute('hidden')) {
						message[j].setAttribute('hidden', true);
					}
				}
			}
		return [newCustomerData, false, id];
	};

	//renders message based on data validity and sends message to backend
	function sendData(URL, data) {
		if (data[1] && data[2] === "customer") {
			resetErrorHighlight(data[2]);
			customerMessage[1].removeAttribute('hidden');
			return;
		} else if (!data[1] && data[2] === "customer") {
			resetErrorHighlight(data[2]);
			customerMessage[0].removeAttribute('hidden');
		}

		if (data[1] && data[2] != "customer") {
			resetErrorHighlight(data[2]);
			tabMessage[1].removeAttribute('hidden');
			return;
		} else if (!data[1] && data[2] != "customer") {
			resetErrorHighlight(data[2]);
			clearField(data[2]);
			tabMessage[0].removeAttribute('hidden');
		}
		fetch(URL, {
            	method: "POST",
            	headers: {
            		'content-type': 'application/json'
            	},
            	body: JSON.stringify(data[0])
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response not ok');
                }
                return response.json();
            });
	};

	//Resets shown messages
	function resetMessage() {
		for (i=0; i<2; i++) {
			customerMessage[i].setAttribute('hidden', true);
			tabMessage[i].setAttribute('hidden', true);
		}
	}

	//
	function resetErrorHighlight(currentForm) {
		if (currentForm === 'customer') {
			if (title.innerText[title.innerText.length-1].toLowerCase() === 's') {
				capitalizedString = title.innerText.toLowerCase().slice(0, -1);
			}
			let tabForm = document.getElementsByClassName(`${capitalizedString}Form`);
			for (i=0;i<tabForm.length;i++) {
				tabForm[i].style.border = "";
			}
		} else {
			let tabForm = document.getElementsByClassName(`customerForm`);
			for (i=0;i<tabForm.length;i++) {
				tabForm[i].style.border = "";
			}
		}
	}

	function clearField(id) {
		if (id[id.length-1] === 's') {
				capitalizedString = id.slice(0, -1);
			}
		let tabForm = document.getElementsByClassName(`${capitalizedString}Form`);
		console.log(tabForm);
		for (i=0;i<tabForm.length;i++) {
			tabForm[i].value = "";
		}
	}

	class CustomerData {
		constructor(customerInfo) {
			this.custNumber = customerInfo[0];
			this.custName = customerInfo[1];
			this.fileName = customerInfo[2];
			this.address1 = customerInfo[4];
			this.address2 = customerInfo[5];
			this.zip = customerInfo[6];
			this.zip4 = customerInfo[7];
			this.city = customerInfo[8];
			this.state = customerInfo[9];
			this.additionalInfo = customerInfo[10];
		}
	}

	class ContactData {
		constructor(contactInfo) {
			this.firstName=contactInfo[0];
			this.lastName=contactInfo[1];
			this.email=contactInfo[2];
			this.phoneNumber=contactInfo[3];
			this.phoneType=contactInfo[4];
		}
	}
});