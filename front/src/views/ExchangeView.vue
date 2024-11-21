<template>
  <div class="exchange-calculator">
    <!-- <h1>어디로 떠나세요?</h1> -->

    <!-- Conversion Form -->
    <div class="form-container">
      <div class="form-group">
        <label for="base-currency">From:</label>
        <select v-model="baseCurrency" id="base-currency">
          <option v-for="rate in rates" :key="rate.cur_unit" :value="rate.cur_unit">
            {{ rate.cur_nm }} ({{ rate.cur_unit }})
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="amount">Amount:</label>
        <input type="number" id="amount" v-model.number="amount" placeholder="Enter amount" />
      </div>

      <div class="form-group">
        <label for="target-currency">To:</label>
        <select v-model="targetCurrency" id="target-currency">
          <option v-for="rate in rates" :key="rate.cur_unit" :value="rate.cur_unit">
            {{ rate.cur_nm }} ({{ rate.cur_unit }})
          </option>
        </select>
      </div>

      <button class="action-button" @click="convertCurrency">Convert</button>
    </div>

    <!-- Conversion Result -->
    <div v-if="convertedAmount !== null" class="result-container">
      <p>{{ amount }} {{ baseCurrency }} = {{ convertedAmount }} {{ targetCurrency }}</p>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-message">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ExchangeCalculator",
  data() {
    return {
      rates: [], // Holds exchange rate data
      baseCurrency: "USD", // Default base currency
      targetCurrency: "KRW", // Default target currency
      amount: 1, // Amount to convert
      convertedAmount: null, // Result of the conversion
      errorMessage: null, // Error message if something goes wrong
    };
  },
  mounted() {
    this.fetchExchangeRates();
  },
  methods: {
    // Fetch exchange rates and handle '(100)' logic
    fetchExchangeRates() {
      axios
        .get("/api/v1/exchange/get/") // Replace with your Django API endpoint
        .then((response) => {
          if (response.data.success) {
            this.rates = response.data.rates.map((item) => {
              const isHundredUnit = item.cur_unit.includes("(100)");
              return {
                cur_unit: isHundredUnit ? item.cur_unit.replace("(100)", "").trim() : item.cur_unit,
                deal_bas_r: parseFloat(item.deal_bas_r.replace(",", "")) * (isHundredUnit ? 1 : 1000000),
                cur_nm: item.cur_nm,
              };
            });
            this.baseCurrency = "KRW";
            this.targetCurrency = "JPY";
          } else {
            this.errorMessage = "Failed to load exchange rates.";
          }
        })
        .catch(() => {
          this.errorMessage = "An error occurred while fetching exchange rates.";
        });
    },

    // Convert currency based on selected options
    convertCurrency() {
      if (!this.amount || !this.baseCurrency || !this.targetCurrency) {
        this.errorMessage = "Please fill out all fields.";
        return;
      }

      const baseRate = this.getRate(this.baseCurrency);
      const targetRate = this.getRate(this.targetCurrency);

      if (baseRate && targetRate) {
        const isBaseHundredUnit = this.isHundredUnit(this.baseCurrency);
        const isTargetHundredUnit = this.isHundredUnit(this.targetCurrency);

        const adjustedBaseRate = isBaseHundredUnit ? baseRate / 100 : baseRate;
        const adjustedTargetRate = isTargetHundredUnit ? targetRate / 100 : targetRate;

        // Perform conversion
        this.convertedAmount = ((this.amount / adjustedBaseRate) * adjustedTargetRate).toFixed(2);
        this.errorMessage = null; // Clear any previous errors
      } else {
        this.errorMessage = "Invalid currency selected.";
      }
    },

    // Helper function to get the deal_bas_r (base rate) for a given currency code
    getRate(currencyCode) {
      const rateObj = this.rates.find((rate) => rate.cur_unit === currencyCode);
      return rateObj ? rateObj.deal_bas_r : null;
    },

    // Helper function to check if a currency uses '(100)'
    isHundredUnit(currencyCode) {
      return this.rates.some((rate) => rate.cur_unit === currencyCode && rate.deal_bas_r >= 10000);
    },
  },
};
</script>

<style scoped>
.exchange-calculator {
  padding: 40px;
  background-color: #FFF8F3; /* Match homepage background */
  max-width: 600px; /* Narrower container */
  margin: 0 auto;
  border-radius: 20px;
}

h1 {
  text-align: center;
  font-size: 2rem;
  color: #706873; /* Match button color */
}

.form-container {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-weight: bold;
  color: #706873; /* Match button color */
}

/* Ensure consistent styling for all input fields and dropdowns */
input,
select {
  width: calc(100% - 20px); /* Consistent width with slight inner padding */
  padding: 10px;
  border-radius: 12px; /* Rounded corners like the button */
  border: none; /* Remove default borders */
  background-color: #f9f9f9; /* Light background for inputs */
  box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
}

/* Add focus effect for better UX */
input:focus,
select:focus {
  outline: none; /* Remove default focus outline */
  box-shadow: inset 0px 2px 4px rgba(0, 0, 0, 0.2); /* Slightly stronger shadow on focus */
}

/* Style the button to match inputs but without a border */
button.action-button {
  background-color: #a5a58d; /* Match homepage button style */
  color: white;
  border-radius: 12px;
  width: 40%;
  margin: 0 auto;
  margin-top: 18px;
  height: 38px;
}

button.action-button:hover {
  background-color: #797967; /* Hover effect */
}

.result-container,
.error-message {
  text-align: center;
}

.result-container p {
  font-size: 1.5rem;
}

.error-message p {
  color: red;
}
</style>