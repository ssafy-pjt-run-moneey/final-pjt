<template>
  <div class="d-flex flex-column align-center">
    <h1 class="my-6 half-highlight">환율 계산기</h1>
    <v-card elevation="10" class="d-flex flex-column align-center pa-10">
      <div>
        <strong v-if="modifiedAt">{{ modifiedAt.substr(0, 10) }}</strong>
        <span v-if="modifiedAt" class="ml-1">기준</span>
      </div>

      <div class="mb-5">
        <p v-if="rate == -1">현재 통화 선택이 유효하지 않습니다.</p>
        <p v-else-if="rate">
          현재 환율은
          <strong>{{ (currencyUnit / rate).toFixed(3) }}</strong>
          입니다.
        </p>
        <p v-else>환전할 통화를 선택하세요.</p>
      </div>

      <!-- 환전 출발 통화 선택 -->
      <v-select
        clearable
        :items="payments"
        v-model="select1"
        class="exchange-select-box"
        label="환전 출발"
        variant="solo-filled"
      ></v-select>

      <!-- 환전 도착 통화 선택 -->
      <v-select
        clearable
        :items="payments"
        v-model="select2"
        class="exchange-select-box"
        label="환전 도착"
        variant="solo-filled"
      ></v-select>

      <!-- 금액 입력 -->
      <div class="mb-4">환전할 금액을 입력하세요.</div>
      <v-text-field
        v-model.number="input_money"
        class="exchange-select-box"
        label="금액"
        variant="solo-filled"
      />

      <!-- 계산 버튼 -->
      <v-chip @click="calculate" class="exchange-cal-btn" elevation="4">
        환율 계산하기
      </v-chip>

      <!-- 계산 결과 출력 -->
      <div class="d-flex flex-column align-center justify-center">
        <p class="mt-5">계산 결과</p>
        <div class="exchange-output">
          {{ output_money.toFixed(2) }} {{ country[select2] }}
        </div>
        <p>입니다.</p>
      </div>
    </v-card>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import axios from "axios";

// 통화 목록 설정
const payments = ref(["KRW", "USD", "JPY", "CNY", "EUR", "TWD", "VND", "GBP", "CHF", "CAD", "AUD", "HKD", "SEK", "NZD", "SGD", "NOK"]);

// 국가별 통화 단위 설정
const country: any = ref({
  KRW: "원",
  USD: "US 달러",
  JPY: "엔",
  CNY: "위안",
  EUR: "유로",
  TWD: "대만달러",
  VND: "동",
  GBP: "파운드",
  CHF: "스위스 프랑",
  CAD: "캐나다 달러",
  AUD: "호주 달러",
});

// 선택된 통화와 환율 정보 관리 변수 설정
const select1 = ref(null);
const select2 = ref(null);
const input_money = ref(0);
const output_money = ref(0);
const rate = ref(null);
const currencyUnit = ref(null);
const modifiedAt = ref(null);

// 두 통화가 선택되었을 때 환율 정보 가져오기
watch([select1, select2], async ([newOption1, newOption2]) => {
  if (newOption1 && newOption2) {
    try {
      // Update the request URL to match Django's /exchange/exchange-rate/ endpoint
      const { data } = await axios.get(`/exchange/exchange-rate/`, {
          params: {
            base_currency: newOption1,
            target_currency: newOption2,
          }
      });

      const baseRate = data.base_currency;
      const targetRate = data.target_currency;

      if (baseRate && targetRate) {
          rate.value = parseFloat(targetRate.deal_bas_r) / parseFloat(baseRate.deal_bas_r);
          currencyUnit.value = 1;  // Adjust this depending on how you want to display it
          modifiedAt.value = new Date().toISOString().substr(0, 10); // Use current date for simplicity
      } else {
          rate.value = -1;
          currencyUnit.value = null;
          modifiedAt.value = null;
      }
      
    } catch (error) {
      console.error("Error fetching exchange rates:", error);
    }
  }
});

// 계산 버튼 클릭 시 금액 변환 로직 실행
const calculate = () => {
  if (rate.value && input_money.value) {
    output_money.value = (input_money.value / rate.value) * currencyUnit.value;
  }
};
</script>

<style lang="scss" scoped>
// 스타일 정의는 그대로 유지합니다.
.exchange-select-box {
  width: 300px;
}

.exchange-cal-btn {
  background-color: #8c704f;
  color: #f2f2f2;
}

.exchange-output {
  font-size: larger;
  font-weight: bold;
}

.half-highlight {
  background: linear-gradient(180deg, rgba(255,255,255,0) 55%, lighten(#59452c,35%) 50%);
}
</style>