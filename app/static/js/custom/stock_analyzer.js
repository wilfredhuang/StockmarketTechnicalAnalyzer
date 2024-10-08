document.addEventListener("DOMContentLoaded", function () {
  loadBootstrapElements();
  loadQuickFillButtons();
  loadFetchDataFeature();
  loadProcessDataFeature();
});

// === Utility Functions ===
function showFlashMessage(category, message) {
  // Function to dynamically add a flash message
  const flashMessageDiv = document.createElement("div");
  flashMessageDiv.className = `alert alert-${category} alert-dismissible fade show mt-2`;
  flashMessageDiv.role = "alert";
  flashMessageDiv.innerHTML = `
${message}
<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
`;

  // Add the new flash message to the #flash-messages div
  document.getElementById("flash-messages").appendChild(flashMessageDiv);

  // Optionally, auto-dismiss the alert after a few seconds
  setTimeout(function () {
    var bsAlert = new bootstrap.Alert(flashMessageDiv);
    bsAlert.close();
  }, 5000); // Dismiss after 5 seconds
}

// === Generic function template to send requests with fetch ===
function sendRequest(url, method, data) {
  return fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        // Handle HTTP errors (e.g., 404, 500)
        throw new Error("Network response was not ok");
      }
      const contentType = response.headers.get("content-type");
      // Check if response contains JSON and parse if so
      if (contentType && contentType.includes("application/json")) {
        return response.json();
      } else if (response.status !== 204) {
        // If not a 204 (No Content), return as text
        return response.text();
      } else {
        return null; // Handle empty response (e.g., 204)
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    });
}

// Handle 'Quick Fill' button click
function handleQuickFill(ticker_data, start_date, end_date) {
  // Example logic for quick fill
  const tickerInput = document.getElementById("ticker");
  const startDateInput = document.getElementById("start");
  const endDateInput = document.getElementById("end");
  tickerInput.value = ticker_data;
  startDateInput.value = start_date;
  endDateInput.value = end_date;
}

// === Load Bootstrap Elements ===
function loadBootstrapElements() {
  // Initialize all Bootstrap tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

// === Minor Event Listeners ===
function loadQuickFillButtons() {
  document
    .getElementById("valid_fetchDataQuickFillBtn")
    .addEventListener("click", function () {
      handleQuickFill(
        "KO, PEP, WMT, SBUX, MCD, AAL, DAL, F, VZ, T, DIS, BAC, JPM, MA, V, ORCL, AMD, NVDA, AAPL, MSFT",
        "2013-12-31",
        "2024-03-31"
      );
    });

  document
    .getElementById("invalidnaming_fetchDataQuickFillBtn")
    .addEventListener("click", function () {
      handleQuickFill(
        "KO1, PEP, WMT, SBUX, MCD, AAL, DAL, F, VZ, T, DIS, BAC, JPM, MA, V, ORCL, AMD, NVDA, AAPL, MSFT2",
        "2013-12-31",
        "2024-03-31"
      );
    });

  document
    .getElementById("invalidlength_fetchDataQuickFillBtn")
    .addEventListener("click", function () {
      handleQuickFill(
        "KO, PEP, WMT, SBUX, MCD, AAL, DAL, F, VZ, T, DIS, BAC, JPM, MA, V, ORCL, AMD, NVDA, AAPL, MSFT, GOOGL, AMZN, NFLX, TSLA, META, INTC, PYPL, CRM, IBM, CSCO, HD",
        "2023-12-31",
        "2014-03-31"
      );
    });
}

// === Main Event Listeners ===
// function loadTestButton() {
//   // Sandbox Button for testing functions purpose only
//   document
//     .getElementById("testing-btn")
//     .addEventListener("click", function () {
//       const testingBtn = document.getElementById("testing-btn");
//       // --Send Request--
//       sendRequest("/sandbox-test-request", "POST", {
//         data: [1, 3, 5, 7, 9],
//       })
//         // --Response Data Handling from server--
//         .then((data) => {
//           // Clear existing flash messages
//           document.getElementById("flash-messages").innerHTML = "";
//           if (data.success) {
//             // If successful, show a success message
//             showFlashMessage("success", data.message);
//             //showFlashMessage('success', 'Your changes have been saved successfully!');
//           } else {
//             // If validation failed, show error message
//             showFlashMessage("danger", data.errors.foobar);
//           }
//         })

//         // --Error Handling--
//         .catch((error) => {
//           console.error("Error:", error);
//           showFlashMessage("danger", "An error occurred.");
//         });
//     });
// }
function loadFetchDataFeature() {
  // Fetch Data to CSV Feature
  document
    .getElementById("fetch-data-btn")
    .addEventListener("click", function () {
      const fetchDataBtn = document.getElementById("fetch-data-btn");

      // Disable the button and show loading state
      fetchDataBtn.disabled = true;
      fetchDataBtn.classList.add("loading-btn");
      // Change button text to 'Loading...' and add a spinner
      fetchDataBtn.innerHTML = `
            <div class="spinner"></div>
            Loading...
        `;

      var data = true;
      const tickerInput = document.getElementById("ticker").value;
      const startDate = document.getElementById("start").value;
      const endDate = document.getElementById("end").value;

      const tickerDropDownBox = document.getElementById("ticker-select");

      if (data != false) {
        sendRequest("/fetch-stock-data", "POST", {
          tickers: tickerInput,
          start_date: startDate,
          end_date: endDate,
        })
          .then((data) => {
            if (data.success) {
              //alert(data.message || data); // Show the message if JSON is returned or text
              showFlashMessage("success", data.message);
              // Clear any existing options from DDB
              tickerDropDownBox.innerHTML = "";
              tickersList = data.tickers_list;

              // Add a placeholder option
              const placeholderOption = document.createElement("option");
              placeholderOption.text = "Select a ticker";
              placeholderOption.value = "";
              tickerDropDownBox.appendChild(placeholderOption);

              // Populate DDB with tickers from backend
              tickersList.forEach((ticker) => {
                const option = document.createElement("option");
                option.text = ticker;
                option.value = ticker;
                tickerDropDownBox.appendChild(option);
              });

              const processDataBtn = (document.getElementById(
                "process-data-btn"
              ).disabled = false);
            } else {
              //alert("No content received.");
              const noOptionsOption = document.createElement("option");
              noOptionsOption.text = "No tickers available";
              noOptionsOption.value = ""; // Optional, depending on how you want to handle this
              tickerDropDownBox.appendChild(noOptionsOption);
              for (i in data.errors) {
                showFlashMessage("danger", data.errors[i]);
              }
            }
          })
          .catch((error) => {
            console.error("Error:", error);
          })
          .finally(() => {
            // Re-enable the button and revert its text and styles
            fetchDataBtn.disabled = false;
            fetchDataBtn.classList.remove("loading-btn");
            fetchDataBtn.innerHTML = "Fetch Data";
          });
      } else {
        //alert("Error");
        showFlashMessage("danger", "An error occurred.");
        // Re-enable the button and revert its text and styles
        fetchDataBtn.disabled = false;
        fetchDataBtn.classList.remove("loading-btn");
        fetchDataBtn.innerHTML = "Fetch Data";
      }
    });
}
function loadProcessDataFeature() {
  // === Process Data Feature ===
  document
    .getElementById("process-data-btn")
    .addEventListener("click", function () {
      const processDataBtn = document.getElementById("process-data-btn");
      const selectedStrategy = document.getElementById("strategy-select").value;
      const selectedTicker = document.getElementById("ticker-select").value;

      // Disable the button and show loading state
      processDataBtn.disabled = true;
      processDataBtn.classList.add("loading-btn");

      // Change button text to 'Loading...' and add a spinner
      processDataBtn.innerHTML = `
          <div class="spinner"></div>
          Loading...
      `;

      sendRequest("/process-stock-data", "POST", {
        strategy: selectedStrategy,
        ticker: selectedTicker,
      })
        .then((data) => {
          if (data && data.image_url) {
            //alert(data.message || data);  // Show the message if JSON is returned or text
            // Update the 'show-graph' div with the new image

            const graphDiv = document.querySelector(".show-graph");
            graphDiv.innerHTML = `<img src="${data.image_url}" alt="Strategy Performance Graph">`;

            const graphDivSecond = document.querySelector(".show-graph-second");
            graphDivSecond.innerHTML = `<img src="${data.image_url_second}" alt="Strategy Performance Comparison Graph">`;

            const nums = data.nums;
            const strat_perf_data = data.strat_perf_data;
            const benchmark_data = data.benchmark_data;

            console.log("Testing123");
            console.log(strat_perf_data);
            console.log(`Each Item is ${nums}`);
            console.log(benchmark_data);

            // === Update Strategy Performance ===
            // Update Performance Statistics
            document.getElementById(
              "sp_total_return_display"
            ).textContent = `${strat_perf_data.total_return}%`;
            document.getElementById(
              "sp_annualised_volatility_display"
            ).textContent = `${strat_perf_data.annualised_volatility}%`;
            document.getElementById(
              "sp_maximum_drawdown_display"
            ).textContent = `${strat_perf_data.maximum_drawdown}%`;
            // Update Trading Activity
            document.getElementById("sp_total_trades_display").textContent =
              strat_perf_data.trades;
            document.getElementById("sp_profit_factor_display").textContent =
              strat_perf_data.profit_factor;
            document.getElementById(
              "sp_average_profit_display"
            ).textContent = `${(strat_perf_data.average_profit * 100).toFixed(
              2
            )}%`;
            document.getElementById(
              "sp_average_loss_display"
            ).textContent = `${(
              strat_perf_data.average_loss_display * 100
            ).toFixed(2)}%`;
            // Update Up/Down Days
            const upDaysProgress = document.getElementById(
              "sp_up_days_progress"
            );
            const downDaysProgress = document.getElementById(
              "sp_down_days_progress"
            );
            upDaysProgress.style.width = `${strat_perf_data.up_days_percentage}%`;
            upDaysProgress.setAttribute(
              "aria-valuenow",
              strat_perf_data.up_days_percentage
            );
            upDaysProgress.textContent = `${strat_perf_data.up_days_percentage}%`;
            downDaysProgress.style.width = `${strat_perf_data.down_days_percentage}%`;
            downDaysProgress.setAttribute(
              "aria-valuenow",
              strat_perf_data.down_days_percentage
            );
            downDaysProgress.textContent = `${strat_perf_data.down_days_percentage}%`;
            document.getElementById(
              "sp_up_days_display"
            ).textContent = `${strat_perf_data.up_days} (${strat_perf_data.up_days_percentage}%)`;
            document.getElementById(
              "sp_down_days_display"
            ).textContent = `${strat_perf_data.down_days} (${strat_perf_data.down_days_percentage}%)`;
            // === Update Benchmark Performance ===
            // Update Benchmark Performance
            document.getElementById(
              "bm_total_return_display"
            ).textContent = `${benchmark_data.total_return}%`;
            document.getElementById(
              "bm_annualised_volatility_display"
            ).textContent = `${benchmark_data.annualised_volatility}%`;
            document.getElementById(
              "bm_maximum_drawdown_display"
            ).textContent = `${benchmark_data.maximum_drawdown}%`;

            // Update Benchmark Trading Activity
            document.getElementById("bm_total_trades_display").textContent =
              benchmark_data.trade_days;
            document.getElementById("bm_profit_factor_display").textContent =
              benchmark_data.profit_factor;
            document.getElementById(
              "bm_average_profit_display"
            ).textContent = `${(benchmark_data.average_profit * 100).toFixed(
              2
            )}%`;
            document.getElementById(
              "bm_average_loss_display"
            ).textContent = `${(benchmark_data.average_loss_display * 100).toFixed(
              2
            )}%`;

            // Update Benchmark Up/Down Days
            const bmUpDaysProgress = document.getElementById(
              "bm_up_days_progress"
            );
            const bmDownDaysProgress = document.getElementById(
              "bm_down_days_progress"
            );

            // Up days progress
            bmUpDaysProgress.style.width = `${benchmark_data.up_days_percentage}%`;
            bmUpDaysProgress.setAttribute(
              "aria-valuenow",
              benchmark_data.up_days_percentage
            );
            bmUpDaysProgress.textContent = `${benchmark_data.up_days_percentage}%`;

            // Down days progress
            bmDownDaysProgress.style.width = `${benchmark_data.down_days_percentage}%`;
            bmDownDaysProgress.setAttribute(
              "aria-valuenow",
              benchmark_data.down_days_percentage
            );
            bmDownDaysProgress.textContent = `${benchmark_data.down_days_percentage}%`;

            // Update list-group items for up and down days display
            document.getElementById(
              "bm_up_days_display"
            ).textContent = `${benchmark_data.up_days} (${benchmark_data.up_days_percentage}%)`;
            document.getElementById(
              "bm_down_days_display"
            ).textContent = `${benchmark_data.down_days} (${benchmark_data.down_days_percentage}%)`;

            // Plotly Chart Generate Here!
            // Inject the returned HTML string for the Plotly graph into the DOM
            //const chartContainer = document.getElementById('chart-container');
            // Parse the JSON string into a JavaScript object
            const figData = JSON.parse(data.graphJSON);
            console.log(
              `FigData is ${figData}, ${figData.data}, ${figData.layout}`
            );

            // Check if the chart already exists
            if (document.getElementById("chart-container").data) {
              document.getElementById("chart-msg").innerHTML = "";
              // Update existing chart
              Plotly.react("chart-container", figData.data, figData.layout);
            } else {
              document.getElementById("chart-msg").innerHTML = "";
              // Create new chart
              Plotly.newPlot("chart-container", figData.data, figData.layout);
            }

            // Re-enable the button and revert its text and styles
            processDataBtn.disabled = false;
            processDataBtn.classList.remove("loading-btn");
            processDataBtn.innerHTML = "Process Data";

            //
          } else {
            // No data received: set all fields to "NIL" or default text
            const noDataMessage = "No data found";

            // === Update Strategy Performance ===
            document.getElementById("sp_total_return_display").textContent =
              noDataMessage;
            document.getElementById(
              "sp_annualised_volatility_display"
            ).textContent = noDataMessage;
            document.getElementById("sp_maximum_drawdown_display").textContent =
              noDataMessage;

            // Update Trading Activity
            document.getElementById("sp_total_trades_display").textContent =
              noDataMessage;
            document.getElementById("sp_profit_factor_display").textContent =
              noDataMessage;
            document.getElementById("sp_average_profit_display").textContent =
              noDataMessage;
            document.getElementById("sp_average_loss_display").textContent =
              noDataMessage;

            // Update Up/Down Days
            const upDaysProgress = document.getElementById(
              "sp_up_days_progress"
            );
            const downDaysProgress = document.getElementById(
              "sp_down_days_progress"
            );

            upDaysProgress.style.width = "0%";
            upDaysProgress.setAttribute("aria-valuenow", "0");
            upDaysProgress.textContent = noDataMessage;

            downDaysProgress.style.width = "0%";
            downDaysProgress.setAttribute("aria-valuenow", "0");
            downDaysProgress.textContent = noDataMessage;

            document.getElementById("sp_up_days_display").textContent =
              noDataMessage;
            document.getElementById("sp_down_days_display").textContent =
              noDataMessage;

            // === Update Benchmark Performance ===
            document.getElementById("bm_total_return_display").textContent =
              noDataMessage;
            document.getElementById(
              "bm_annualised_volatility_display"
            ).textContent = noDataMessage;
            document.getElementById("bm_maximum_drawdown_display").textContent =
              noDataMessage;

            // Update Benchmark Trading Activity
            document.getElementById("bm_total_trades_display").textContent =
              noDataMessage;
            document.getElementById("bm_profit_factor_display").textContent =
              noDataMessage;
            document.getElementById("bm_average_profit_display").textContent =
              noDataMessage;
            document.getElementById("bm_average_loss_display").textContent =
              noDataMessage;

            // Update Benchmark Up/Down Days
            const bmUpDaysProgress = document.getElementById(
              "bm_up_days_progress"
            );
            const bmDownDaysProgress = document.getElementById(
              "bm_down_days_progress"
            );

            bmUpDaysProgress.style.width = "0%";
            bmUpDaysProgress.setAttribute("aria-valuenow", "0");
            bmUpDaysProgress.textContent = noDataMessage;

            bmDownDaysProgress.style.width = "0%";
            bmDownDaysProgress.setAttribute("aria-valuenow", "0");
            bmDownDaysProgress.textContent = noDataMessage;

            document.getElementById("bm_up_days_display").textContent =
              noDataMessage;
            document.getElementById("bm_down_days_display").textContent =
              noDataMessage;

            // Price Chart
            document.getElementById("chart-msg").innerHTML = "No data found";

            alert("No content received.");

            // Disable the button and revert its text and styles
            processDataBtn.disabled = true;
            processDataBtn.classList.remove("loading-btn");
            processDataBtn.innerHTML = "Process Data";
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        })
        .finally(() => {console.log("Finished")});

      console.log("Clicked 2");
    });
}
