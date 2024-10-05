document.addEventListener("DOMContentLoaded", function () {
  // Bootstrap Tab (JS Code for this may not be needed)
  const tabs = document.querySelectorAll(".nav-link");
  const tabContents = document.querySelectorAll(".tab-pane");

  tabs.forEach((tab) => {
    tab.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent default anchor click behavior

      // Remove active class from all tabs and hide all tab contents
      tabs.forEach((t) => t.classList.remove("active"));
      tabContents.forEach((content) =>
        content.classList.remove("show", "active")
      );

      // Add active class to the clicked tab and show corresponding content
      this.classList.add("active");
      const target = document.querySelector(this.getAttribute("href"));
      target.classList.add("show", "active");
    });
  });
  //

  // Generic function template to send requests with fetch
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

  // Fetch Data Feature
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

      sendRequest("/fetch-stock-data", "POST", {})
        .then((data) => {
          if (data) {
            alert(data.message || data); // Show the message if JSON is returned or text
          } else {
            alert("No content received.");
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

      console.log("Clicked");
    });

  // Process Data Feature
  document
    .getElementById("process-data-btn")
    .addEventListener("click", function () {
      const processDataBtn = document.getElementById("process-data-btn");
      const selectedStrategy = document.getElementById("strategy-select").value;

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
      })
        .then((data) => {
          if (data && data.image_url) {
            //alert(data.message || data);  // Show the message if JSON is returned or text
            // Update the 'show-graph' div with the new image

            const graphDiv = document.querySelector(".show-graph");
            graphDiv.innerHTML = `<img src="${data.image_url}" alt="Strategy Performance Graph">`;

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
            ).textContent = `${strat_perf_data.average_profit}%`;
            document.getElementById(
              "sp_average_loss_display"
            ).textContent = `${strat_perf_data.average_loss_display}%`;
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
            ).textContent = `${benchmark_data.average_profit}%`;
            document.getElementById(
              "bm_average_loss_display"
            ).textContent = `${benchmark_data.average_loss_display}%`;

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
            console.log(`FigData is ${figData}, ${figData.data}, ${figData.layout}`)
                    
            // Check if the chart already exists
            if (document.getElementById('chart-container').data) {
                // Update existing chart
                Plotly.react('chart-container', figData.data, figData.layout);
            } else {
                // Create new chart
                Plotly.newPlot('chart-container', figData.data, figData.layout);
            }

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
            alert("No content received.");
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        })
        .finally(() => {
          // Re-enable the button and revert its text and styles
          processDataBtn.disabled = false;
          processDataBtn.classList.remove("loading-btn");
          processDataBtn.innerHTML = "Process Data";
        });

      console.log("Clicked 2");
    });
});
