<template>
  <div class="exchange-calculator">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <template v-else>
      <div class="current-rate" v-if="amount && convertedAmount">
        {{ amount }} {{ formatCurrencyCode(fromCurrency) }} = {{ convertedAmount }} {{ formatCurrencyCode(toCurrency) }}
        <div class="update-time">{{ lastUpdated }}</div>
      </div>
      <div class="conversion-form">
        <div class="input-group">
          <input 
            type="number" 
            v-model.number="amount" 
            @input="forwardConversion"
            placeholder="Enter amount"
          />
          <select v-model="fromCurrency" @change="forwardConversion">
            <option value="KRW">대한민국 원 (KRW)</option>
          </select>
        </div>

        <div class="input-group">
          <input 
            type="number" 
            v-model.number="convertedAmount" 
            @input="reverseConversion"
            placeholder="Enter amount"
          />
          <select v-model="toCurrency" @change="forwardConversion">
            <option v-for="currency in currencies" 
                    :key="currency.cur_unit" 
                    :value="currency.cur_unit">
              {{ currency.cur_nm }} ({{ formatCurrencyCode(currency.cur_unit) }})
            </option>
          </select>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ExchangeCalculator',
  data() {
    return {
      amount: 1000,
      convertedAmount: 0,
      fromCurrency: 'KRW',
      toCurrency: 'USD',
      currencies: [],
      lastUpdated: '',
      selectedRate: null,
      loading: true,
      error: null
    }
  },
  async mounted() {
    await this.fetchExchangeRates();
    if (!this.error) {
      this.forwardConversion();
    }
  },
  methods: {
    async fetchExchangeRates() {
      try {
        const response = await axios.get('/api/v1/exchange/get/');
        if (response.data.success) {
          this.currencies = response.data.rates;
          const date = new Date(response.data.date);
          this.lastUpdated = `${date.toLocaleDateString()} ${date.toLocaleTimeString()} UTC`;
        } else {
          throw new Error(response.data.error || 'Failed to fetch rates');
        }
      } catch (error) {
        this.error = 'Failed to fetch rates: ' + error.message;
        console.error(this.error);
      } finally {
        this.loading = false;
      }
    },
    formatCurrencyCode(code) {
      return code.replace('(100)', '');
    },
    calculateRate() {
      const fromRate = this.currencies.find(c => c.cur_unit === this.fromCurrency);
      const toRate = this.currencies.find(c => c.cur_unit === this.toCurrency);
      
      if (fromRate && toRate) {
        const fromValue = parseFloat(fromRate.deal_bas_r.replace(",", ""));
        const toValue = parseFloat(toRate.deal_bas_r.replace(",", ""));
        
        let rate = toValue / fromValue;
        
        if (fromRate.cur_unit.includes('(100)')) {
          rate = rate * 100;
        }
        if (toRate.cur_unit.includes('(100)')) {
          rate = rate / 100;
        }
        
        return rate.toFixed(5);
      }
      return null;
    },
    async forwardConversion() {
      if (!this.amount) return;
      
      try {
        const response = await axios.get('/api/v1/exchange/convert/', {
          params: {
            amount: this.amount,
            from_currency: this.fromCurrency,
            to_currency: this.toCurrency
          }
        });
        
        if (response.data.success) {
          this.convertedAmount = parseFloat(response.data.converted_amount).toFixed(2);
          this.selectedRate = this.calculateRate();
        } else {
          throw new Error(response.data.error || 'Conversion failed');
        }
      } catch (error) {
        console.error('Conversion failed:', error);
        this.error = 'Conversion failed: ' + error.message;
      }
    },
    async reverseConversion() {
      if (!this.convertedAmount) return;
      
      try {
        const response = await axios.get('/api/v1/exchange/convert/', {
          params: {
            amount: this.convertedAmount,
            from_currency: this.toCurrency,
            to_currency: this.fromCurrency
          }
        });
        
        if (response.data.success) {
          this.amount = parseFloat(response.data.converted_amount).toFixed(2);
          this.selectedRate = this.calculateRate();
        } else {
          throw new Error(response.data.error || 'Conversion failed');
        }
      } catch (error) {
        console.error('Conversion failed:', error);
        this.error = 'Conversion failed: ' + error.message;
      }
    }
  }
}
</script>

<style scoped>
.exchange-calculator {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.current-rate {
  text-align: center;
  font-size: 1.2em;
  margin-bottom: 20px;
}

.update-time {
  font-size: 0.8em;
  color: #666;
  margin-top: 5px;
}

.conversion-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.input-group {
  display: flex;
  gap: 10px;
}

input {
  flex: 1;
  padding: 8px;
  border: 1px solid #d3d3d3;
  border-radius: 6px;
  font-size: 14px;
}

select {
  padding: 8px;
  border: 1px solid #d3d3d3;
  border-radius: 6px;
  font-size: 14px;
  min-width: 150px;
}

input:focus,
select:focus {
  outline: none;
  border-color: #706873;
}

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}
</style>