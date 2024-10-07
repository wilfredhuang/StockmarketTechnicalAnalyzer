document.addEventListener("DOMContentLoaded", function () {
  // Initialize all Bootstrap tooltips
  initializeTooltips();

  // Event listeners for buttons
  document.getElementById("testing-btn").addEventListener("click", handleSandboxRequest);
  document.getElementById("fetch-data-btn").addEventListener("click", handleFetchData);
  document.getElementById("process-data-btn").addEventListener("click", handleProcessData);
});

// === Constants ===
const FLASH_MESSAGES_DIV = document.getElementById("flash-messages");
const TICKER_INPUT = document.getElementById("ticker");
const START_DATE_INPUT = document.getElementById("start");
const END_DATE_INPUT = document.getElementById("end");
const STRATEGY_SELECT = document.getElementById("strategy-select");

// === Initialization Functions ===
function initializeTooltips() {
  const tooltipTriggerList = [].slice.call(
      document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
      new bootstrap.Tooltip(tooltipTriggerEl);
  });
}

// === Spinner Functions ===
function showSpinner() {
  document.getElementById("spinner").style.display = "block";
}

function hideSpinner() {
  document.getElementById("spinner").style.display = "none";
}

// === Request Functions ===
function sendRequest(url, method, data) {
  return fetch(url, {
      method: method,
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
  })
      .then((response) => handleResponse(response))
      .catch((error) => handleError(error));
}

function handleResponse(response) {
  if (!response.ok) {
      throw new Error("Network response was not ok");
  }
  const contentType = response.headers.get("content-type");
  if (contentType && contentType.includes("application/json")) {
      return response.json();
  } else if (response.status !== 204) {
      return response.text();
  } else {
      return null; // Handle empty response (e.g., 204)
  }
}

function handleError(error) {
  console.error("Error:", error);
  alert("An error occurred. Please try again.");
}

// === Button Handlers ===
function handleSandboxRequest() {
  const sandboxBtn = document.getElementById("testing-btn");
  const spinner = document.getElementById("spinner");
  const btnText = sandboxBtn.querySelector("#btn-text");

  // Show spinner and disable button before starting the request
  sandboxBtn.disabled = true;
  spinner.style.display = "inline-block";
  btnText.textContent = "Loading...";

  sendRequest("/sandbox-test-request", "POST", { data: [1, 3, 5, 7, 9] })
      .then((data) => handleSandboxResponse(data))
      .catch(handleError)
      .finally(() => {
          // Hide spinner and re-enable button after request
          spinner.style.display = "none";
          btnText.textContent = "Run Test";
          sandboxBtn.disabled = false;
      });
}

function handleSandboxResponse(data) {
  // Clear existing flash messages
  FLASH_MESSAGES_DIV.innerHTML = "";
  
  if (data.success) {
      showFlashMessage("success", data.message);
  } else {
      showFlashMessage("danger", data.errors.foobar || "An error occurred");
  }
}

function handleFetchData() {
  const fetchDataBtn = document.getElementById("fetch-data-btn");
  const spinner = document.getElementById("spinner");
  const btnText = document.getElementById("btn-text");

  // Show spinner and disable button before starting the request
  fetchDataBtn.disabled = true;
  spinner.style.display = "inline-block";
  btnText.textContent = "Loading...";

  const formData = getFetchFormData();
  if (!formData) {
      // Hide spinner and re-enable button if validation fails
      spinner.style.display = "none";
      btnText.textContent = "Fetch Data";
      fetchDataBtn.disabled = false;
      return;
  }

  sendRequest("/fetch-stock-data", "POST", {
      tickers: formData.tickers,
      start_date: formData.startDate,
      end_date: formData.endDate,
  })
      .then(handleFetchDataResponse)
      .catch(handleError)
      .finally(() => {
          // Hide spinner and re-enable button after request
          spinner.style.display = "none";
          btnText.textContent = "Fetch Data";
          fetchDataBtn.disabled = false;
      });
}

function handleFetchDataResponse(data) {
  if (data.success) {
      showFlashMessage("success", data.message);
  } else {
      data.errors.forEach((error) => showFlashMessage("danger", error));
  }
}

function handleProcessData() {
  const processDataBtn = document.getElementById("process-data-btn");
  showSpinner(); // Show spinner before starting the request

  const selectedStrategy = STRATEGY_SELECT.value;

  sendRequest("/process-stock-data", "POST", { strategy: selectedStrategy })
      .then(handleProcessDataResponse)
      .catch(handleError)
      .finally(hideSpinner); // Ensure spinner is hidden after the request
}

function handleProcessDataResponse(data) {
  if (data && data.image_url) {
      updateStrategyPerformance(data.strat_perf_data);
      updateBenchmarkPerformance(data.benchmark_data);
      plotGraph(data.graphJSON);
  } else {
      handleNoDataReceived();
  }
}

// === Utility Functions ===
function toggleLoadingState(button, loadingText) {
  const isLoading = button.disabled;
  button.disabled = !isLoading;
  button.classList.toggle("loading-btn", !isLoading);
  button.innerHTML = isLoading
      ? loadingText
      : button.dataset.originalText || button.innerHTML;
  if (isLoading) {
      button.dataset.originalText = button.innerHTML; // Store original text
  }
}

function getFetchFormData() {
  const tickerInput = TICKER_INPUT.value;
  const tickerRegex = /^[A-Z,]+$/;

  if (!tickerRegex.test(tickerInput)) {
      alert("Please enter only capital letters and commas in the ticker field.");
      return false;
  }

  const tickersArray = tickerInput.split(",").map(ticker => ticker.trim()).filter(Boolean);

  if (tickersArray.length === 0 || tickersArray.length > 20) {
      alert("Please enter a valid number of tickers (1-20).");
      return false;
  }

  const currentDate = new Date().toISOString().split("T")[0];
  const startDate = START_DATE_INPUT.value;
  const endDate = END_DATE_INPUT.value;

  if (!startDate || !endDate || startDate > currentDate || endDate > currentDate || endDate < startDate) {
      alert("Invalid date range.");
      return false;
  }

  return { tickers: tickersArray, startDate, endDate };
}

function showFlashMessage(category, message) {
  const flashMessageDiv = document.createElement("div");
  flashMessageDiv.className = `alert alert-${category} alert-dismissible fade show mt-2`;
  flashMessageDiv.role = "alert";
  flashMessageDiv.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
  `;
  FLASH_MESSAGES_DIV.appendChild(flashMessageDiv);

  setTimeout(() => {
      const bsAlert = new bootstrap.Alert(flashMessageDiv);
      bsAlert.close();
  }, 5000); // Dismiss after 5 seconds
}

// === Performance Update Functions ===
function updateStrategyPerformance(performanceData) {
  document.getElementById("sp_total_return_display").textContent = `${performanceData.total_return}%`;
  document.getElementById("sp_annualised_volatility_display").textContent = `${performanceData.annualised_volatility}%`;
  document.getElementById("sp_maximum_drawdown_display").textContent = `${performanceData.maximum_drawdown}%`;
  document.getElementById("sp_total_trades_display").textContent = performanceData.trades;
  document.getElementById("sp_profit_factor_display").textContent = performanceData.profit_factor;
  document.getElementById("sp_average_profit_display").textContent = `${performanceData.average_profit}%`;
  document.getElementById("sp_average_loss_display").textContent = `${performanceData.average_loss_display}%`;

  updateDaysProgress(performanceData.up_days_percentage, "sp");
  updateDaysProgress(performanceData.down_days_percentage, "sp");
}

function updateBenchmarkPerformance(benchmarkData) {
  document.getElementById("bm_total_return_display").textContent = `${benchmarkData.total_return}%`;
  document.getElementById("bm_annualised_volatility_display").textContent = `${benchmarkData.annualised_volatility}%`;
  document.getElementById("bm_maximum_drawdown_display").textContent = `${benchmarkData.maximum_drawdown}%`;
  document.getElementById("bm_total_trades_display").textContent = benchmarkData.trade_days;
  document.getElementById("bm_profit_factor_display").textContent = benchmarkData.profit_factor;
  document.getElementById("bm_average_profit_display").textContent = `${benchmarkData.average_profit}%`;
  document.getElementById("bm_average_loss_display").textContent = `${benchmarkData.average_loss_display}%`;

  updateDaysProgress(benchmarkData.up_days_percentage, "bm");
  updateDaysProgress(benchmarkData.down_days_percentage, "bm");
}

function updateDaysProgress(percentage, prefix) {
  const progressBar = document.getElementById(`${prefix}_up_days_progress`);
  progressBar.style.width = `${percentage}%`;
  progressBar.setAttribute("aria-valuenow", percentage);
  progressBar.textContent = `${percentage}%`;
  document.getElementById(`${prefix}_up_days_display`).textContent = `${percentage} days`;
}

function plotGraph(graphJSON) {
  const figData = JSON.parse(graphJSON);
  const chartContainer = document.getElementById("chart-container");
  if (chartContainer.data) {
      Plotly.react("chart-container", figData.data, figData.layout);
  } else {
      Plotly.newPlot("chart-container", figData.data, figData.layout);
  }
}

function handleNoDataReceived() {
  const noDataMessage = "No data found";
  // Update strategy and benchmark displays with no data message
  updateStrategyPerformance({ total_return: noDataMessage });
  updateBenchmarkPerformance({ total_return: noDataMessage });
}
