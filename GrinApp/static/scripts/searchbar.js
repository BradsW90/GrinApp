document.addEventListener("DOMContentLoaded", function () {
    //Get reference to Customer searchbar
	const addServiceSearch = document.getElementById('customerNameSelect');
    //Gets reference to element used to render suggestions
    const suggestions = document.getElementById('suggestion');
    //Gets direct reference to form wrapping customer
    const customerForm = document.getElementById('form');
    //used to track highlight in suggestions
    var highlight = -1;


    //grabs customer name and numbers for suggesting
    function predictionData() {
        $.ajax({
            url: `/preAddService/`,
            method: 'GET',
            success: function (response) {
                data = response.data;
            },
            error: function (error) {
                console.log('Error:', error);
            }
        });
    }


    //clears all populated suggestions
    function clearSuggestions() {
        while (suggestions.firstChild) {
            suggestions.removeChild(suggestions.firstChild);
        }
    }


    //handles form submit for top section
    //if user has customer highlighted puts value in searchbar and submits otherwise submits whats already in searchbar
    customerForm.addEventListener('submit', function(e) {
        e.preventDefault()
        const suggestionOptions = document.querySelectorAll('#suggestion li');
        if (highlight != -1) {
            addServiceSearch.value = suggestionOptions[highlight].innerText;
            highlight = -1;
            form.submit();
        }
        form.submit();
    });


    //handles population of suggestions based on user input
    addServiceSearch.addEventListener('input', () => {
        highlight = -1;
        let filter = [];
        clearSuggestions();
        data.forEach((customer) => {
            if (customer.CustomerName != null && customer.CustomerNumber != null && addServiceSearch.value != "") {
                if (customer.CustomerName.toLowerCase().startsWith(addServiceSearch.value.toLowerCase()) || customer.CustomerNumber.startsWith(addServiceSearch.value)) {
                    filter.push(customer.CustomerName);
                }
            }
        });
        if (filter.length === 1 && filter[0].toLowerCase() === addServiceSearch.value.toLowerCase()) {
        filter = [];
        }
        filter.forEach((item) => {
            let el = document.createElement('li')
            el.textContent = item;
            suggestions.appendChild(el);
        });
    });


    //handles function to arrow down and up through suggestions
    addServiceSearch.addEventListener('keydown', function (e) {
        const suggestionOptions = document.querySelectorAll('#suggestion li');
        if (e.key === "ArrowDown" && addServiceSearch.value != "") {
            if (highlight === -1) {
                highlight += 1;
                suggestionOptions[highlight].style.backgroundColor = "rgba(73, 212, 32, .3)";
            } else if (highlight >= 0 && highlight < suggestionOptions.length -1) {
                highlight += 1;
                suggestionOptions[highlight].style.backgroundColor = "rgba(73, 212, 32, .3)";
                suggestionOptions[highlight-1].style.backgroundColor = "";
            }
        }
        if (e.key === "ArrowUp" && addServiceSearch.value != "") {
            if (highlight > 0) {
                highlight -= 1;
                suggestionOptions[highlight].style.backgroundColor = "rgba(73, 212, 32, .3)";
                suggestionOptions[highlight+1].style.backgroundColor = "";
            }
        }
    });


    //resets arrowed inputs on mouse over
    suggestions.addEventListener('mouseover', function() {
        const suggestionOptions = document.querySelectorAll("#suggestion li");
        suggestionOptions.forEach(function(el) {
            el.style.backgroundColor = "";
            highlight = -1;
        });
    });


    //populates search bar with clicked suggestion contents
    suggestions.addEventListener('click', function (e) {
        addServiceSearch.value = e.target.innerText;
        clearSuggestions();
        form.submit();
    });

    predictionData();
})