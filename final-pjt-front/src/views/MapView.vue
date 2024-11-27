<template>
  <div class="map-container">
    <!-- Left Search Panel -->
    <div class="search-panel">
      <div class="search-form">
        <div class="select-group">
          <select v-model="province" @change="updateCities">
            <option value="">도/시 선택</option>
            <option v-for="info in infos" :key="info.id" :value="info.prov">
              {{ info.prov }}
            </option>
          </select>

          <select v-model="city">
            <option value="">시/군/구 선택</option>
            <option v-for="c in cities" :key="c" :value="c">
              {{ c }}
            </option>
          </select>

          <select v-model="bank">
            <option value="">은행 선택</option>
            <option v-for="b in banks" :key="b" :value="b">
              {{ b }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Right Map Panel -->
    <div class="map-panel">
      <MapComponent 
        ref="mapComponent"
        :province="province"
        :city="city"
        :bank="bank"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import MapComponent from '@/components/MapComponent.vue'
import { useMapStore } from '@/stores/map'

const store = useMapStore()
const mapComponent = ref(null)

const infos = store.infos
const banks = store.banks
const cities = ref([])

const province = ref('')
const city = ref('')
const bank = ref('')

const updateCities = () => {
  const selectedInfo = infos.find((info) => info.prov === province.value)
  cities.value = selectedInfo ? selectedInfo.city : []
}

const searchBanks = () => {
  if (!province.value || !city.value || !bank.value) {
    alert('모든 항목을 선택해주세요.')
    return
  }
  // Trigger search in MapComponent
  mapComponent.value?.searchLocation()
}
</script>

<style scoped>
.map-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.select-group {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

select {
  padding: 8px 12px;
  border: 1px solid #d3d3d3;
  border-radius: 6px;
  font-size: 14px;
  background-color: white;
  min-width: 150px;
  cursor: pointer;
}

select:hover {
  border-color: #706873;
}

.map-wrapper {
  width: 100%;
  height: 600px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .select-panel {
    flex-direction: column;
    align-items: stretch;
  }

  select {
    width: 100%;
  }
}
</style>