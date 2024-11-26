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
            <div style="padding: 15px; min-width: 250px; text-align: center; border-radius: 8px; font-family: Arial, sans-serif;">
              <h3 style="margin: 0 0 10px 0; font-size: 16px; color: #47413b;">
                ${place.place_name}
              </h3>
              <hr style="border: none; height: 1px; background-color: #DDBEA9; margin: 10px 0;">
              <div style="text-align: left; font-size: 13px; color: #666;">
                <p style="margin: 8px 0;">
                  <span style="color: #A5A58D; font-weight: bold;">주소:</span> ${place.address_name}
                </p>
                ${place.phone ? 
                  `<p style="margin: 8px 0;">
                    <span style="color: #A5A58D; font-weight: bold;">전화:</span> ${place.phone}
                  </p>` 
                  : ''
                }
                ${place.operating_hours ? 
                  `<p style="margin: 8px 0;">
                    <span style="color: #A5A58D; font-weight: bold;">영업시간:</span> ${place.operating_hours}
                  </p>`
                  : ''
                }
              </div>
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