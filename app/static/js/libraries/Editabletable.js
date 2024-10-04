
// Function to delete a ticker
function deleteTicker(tickerId) {
    // Confirm deletion
    if (confirm("Are you sure you want to delete this ticker?")) {
        fetch(`/delete_ticker/${tickerId}`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrf_access_token')  // Include CSRF token if required
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                console.log('Success:', data.message);
                // Optionally remove the ticker row from the DOM
                document.querySelector(`tr[data-ticker-id="${tickerId}"]`).remove();
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
}

// Function to toggle the display of the ticker container
function toggleTickerDisplay() {
    const tickerContainer = document.getElementById('tickerContainer');
    const sellContainer = document.getElementById('sellContainer');
    
    // Toggle the display property
    if (tickerContainer.style.display === 'none' || tickerContainer.style.display === '') {
        tickerContainer.style.display = 'block';
        sellContainer.style.display = 'none';

    } else {
        tickerContainer.style.display = 'none';
    }
}

// Function to toggle the display of the ticker container
function toggleSellDisplay() {
    const sellContainer = document.getElementById('sellContainer');
    const tickerContainer = document.getElementById('tickerContainer');
    
    // Toggle the display property
    if (sellContainer.style.display === 'none' || sellContainer.style.display === '') {
        sellContainer.style.display = 'block';
        tickerContainer.style.display = 'none';
    } else {
        sellContainer.style.display = 'none';
    }
}
// Add event listener to the button
document.getElementById('addTickerButton').addEventListener('click', toggleTickerDisplay);

// Add event listener to the button
document.getElementById('soldSharesButton').addEventListener('click', toggleSellDisplay);

//toggle for add ticker textbox or dropdown
function toggleInput() {
    var dropdown = document.getElementById('existing-ticker');
    var textInput = document.getElementById('new-ticker');
    var toggleButton = document.getElementById('toggleButton');
    
    // Toggle visibility of dropdown and textbox
    if (dropdown.style.display === 'none') {
        dropdown.style.display = 'block';
        textInput.style.display = 'none';
        toggleButton.innerText = 'Enter New Stock';  // Change button text to indicate that the user can enter a new ticker
        dropdown.required = true; // Set dropdown as required
        dropdown.disabled = false; // Enable the dropdown
        textInput.required = false; // Remove requirement from text input
    } else {
        dropdown.style.display = 'none';
        textInput.style.display = 'block';
        toggleButton.innerText = 'Select Existing Stock';  // Change button text to indicate that the user can select an existing ticker
        dropdown.required = false; // Remove requirement from dropdown
        dropdown.disabled = true; // Disable the dropdown
        textInput.required = true; // Set text input as required
    }
}


// Function to get CSRF token from cookies (if using Flask-WTF)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//For piechart
document.addEventListener("DOMContentLoaded", function () {
    // Get data from the hidden div
    const chartDataElement = document.getElementById("chartData");

    // Parse the JSON data stored in the data attributes
    const ticker_data = JSON.parse(chartDataElement.getAttribute("data-ticker"));
    const shares_data = JSON.parse(chartDataElement.getAttribute("data-shares"));

    // Log the data for debugging purposes
    console.log(ticker_data, shares_data);

    // Create the pie chart
    new Chart(document.getElementById("myChart"), {
        type: "pie",
        data: {
            labels: ticker_data.flat(),
            datasets: [{
                data: shares_data.flat(),
                fill: false,
                lineTension: 0.1
            }]
        },
        options: {
            responsive: false,  // Disable responsiveness to manually control size
            maintainAspectRatio: false,  // Allow changing the aspect ratio
        }
    });
});