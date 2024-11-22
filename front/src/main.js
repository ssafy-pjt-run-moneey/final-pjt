import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createVuetify } from 'vuetify'
import { VSelect, VTextField, VChip, VCard } from 'vuetify/components'
import * as directives from 'vuetify/directives'
import App from './App.vue'
import router from './router'
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8000'; //
const app = createApp(App)
const pinia = createPinia()
const vuetify = createVuetify({
  components: {
    VSelect,
    VTextField,
    VChip,
    VCard
  },
  directives
})



// Vue.config.devtools = true;
pinia.use(piniaPluginPersistedstate)
// app.use(createPinia())
app.use(pinia)
app.use(router)
app.use(vuetify)
app.mount('#app')
app.config.compilerOptions.isCustomElement = tag => tag.startsWith('ion-')