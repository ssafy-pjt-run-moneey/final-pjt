<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  province: String,
  city: String,
  bank: String
})

const mapContainer = ref(null)
const map = ref(null)
const markers = ref([])
const infowindows = ref([])

onMounted(() => {
  initializeMap()
})

const initializeMap = () => {
  if (!window.kakao) {
    const script = document.createElement('script')
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=5b26ecb0711f7c8797946df3ca9dc6a0&libraries=services&autoload=false`
    document.head.appendChild(script)

    script.onload = () => {
      window.kakao.maps.load(() => {
        createMap()
      })
    }
  } else {
    createMap()
  }
}

const createMap = () => {
  const options = {
    center: new window.kakao.maps.LatLng(37.5665, 126.9780), // Seoul coordinates
    level: 3
  }
  map.value = new window.kakao.maps.Map(mapContainer.value, options)
}

const searchBanks = () => {
  if (!props.province || !props.city || !props.bank) return

  const places = new window.kakao.maps.services.Places()
  const searchQuery = `${props.province} ${props.city} ${props.bank}`

  places.keywordSearch(searchQuery, (result, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      clearMarkersAndInfowindows()
      
      // Create bounds to fit all markers
      const bounds = new window.kakao.maps.LatLngBounds()
      
      result.forEach(place => {
        const position = new window.kakao.maps.LatLng(place.y, place.x)
        
        // Create a custom marker image
        const markerImage = new window.kakao.maps.MarkerImage(
          '/gal.png',
          new window.kakao.maps.Size(64, 69),
          { offset: new window.kakao.maps.Point(27, 69) }
        )
        
        // Create marker
        const marker = new window.kakao.maps.Marker({
          map: map.value,
          position: position
        })
        
        // Create infowindow
        const infowindow = new window.kakao.maps.InfoWindow({
          content: `
            <div style="padding:8px;font-size:15px;">
              ${place.place_name}<br>
              ${place.address_name}<br>
              ${place.phone ? `${place.phone}<br>` : ''}<br>
            </div>
          `
        })
        
        // Add click event to marker
        window.kakao.maps.event.addListener(marker, 'click', () => {
          infowindows.value.forEach(iw => iw.close())
          infowindow.open(map.value, marker)
        })
        
        markers.value.push(marker)
        infowindows.value.push(infowindow)
        bounds.extend(position)
      })
      
      // Fit map to show all markers
      map.value.setBounds(bounds)
    }
  })
}

const clearMarkersAndInfowindows = () => {
  markers.value.forEach(marker => marker.setMap(null))
  infowindows.value.forEach(infowindow => infowindow.close())
  markers.value = []
  infowindows.value = []
}

// Watch for changes in props
watch([() => props.province, () => props.city, () => props.bank], () => {
  if (props.province && props.city && props.bank) {
    searchBanks()
  }
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
  min-height: 600px;
  border-radius: 12px;
}
</style>