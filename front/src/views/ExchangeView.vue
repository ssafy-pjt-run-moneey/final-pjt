<template>
  <div class="exchange-calculator">
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
      selectedRate: null
    }
  },
  mounted() {
    this.fetchExchangeRates();
  },
  methods: {
    async fetchExchangeRates() {
      try {
        const response = await axios.get('/api/v1/exchange/get/');
        if (response.data.success) {
          this.currencies = response.data.rates;
          this.updateConversion();
          const date = new Date();
          this.lastUpdated = `${date.toLocaleDateString()} ${date.toLocaleTimeString()} UTC`;
        }
      } catch (error) {
        console.error('Failed to fetch rates:', error);
      }
    },
    async updateConversion() {
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
          this.convertedAmount = response.data.converted_amount;
          this.selectedRate = this.calculateRate();
        }
      } catch (error) {
        console.error('Conversion failed:', error);
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
        
        // Adjust rate for currencies with (100) notation
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

    async updateConversion() {
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
          // For currencies with (100), adjust the display
          if (this.toCurrency.includes('(100)')) {
            this.convertedAmount = (response.data.converted_amount * 100).toFixed(2);
          } else {
            this.convertedAmount = response.data.converted_amount;
          }
          this.selectedRate = this.calculateRate();
        }
      } catch (error) {
        console.error('Conversion failed:', error);
      }
    },
    // 위쪽 입력창에서 계산 (KRW → 외화)
    async forwardConversion() {
      if (!this.amount) return;
      
      const toRate = this.currencies.find(c => c.cur_unit === this.toCurrency);
      if (toRate) {
        const rate = parseFloat(toRate.deal_bas_r.replace(",", ""));
        const mod = this.toCurrency.includes('(100)') ? 100 : 1;
        
        // 원화 금액 / 해당 통화의 deal_bas_r × mod값
        this.convertedAmount = ((this.amount / rate) * mod).toFixed(2);
        this.selectedRate = (1 / rate * mod).toFixed(5);
      }
    },

    // 아래쪽 입력창에서 계산 (외화 → KRW)
    async reverseConversion() {
      if (!this.convertedAmount) return;
      
      const toRate = this.currencies.find(c => c.cur_unit === this.toCurrency);
      if (toRate) {
        const rate = parseFloat(toRate.deal_bas_r.replace(",", ""));
        const mod = this.toCurrency.includes('(100)') ? 100 : 1;
        
        // 외화 금액 × 해당 통화의 deal_bas_r / mod값
        this.amount = (this.convertedAmount * rate / mod).toFixed(2);
        this.selectedRate = (1 / rate * mod).toFixed(5);
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