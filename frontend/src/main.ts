import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import axios from 'axios'
import { getCookie } from 'typescript-cookie'

import App from './App.vue'
import router from './router'
import { useUserStore } from "./stores/users"

// Pinia init
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)

axios.defaults.withCredentials = true
axios.defaults.baseURL = 'http://localhost:8000/'

// CSRF token
axios.interceptors.request.use(function (config: any) {
  if (
    ["POST", "PUT", "DELETE", "PATCH"].indexOf(
      config.method.toUpperCase()
    ) != -1
  ) {
    const csrfToken = getCookie("csrftoken")
    config.headers["X-CSRFToken"] = csrfToken
  }
  return config
})

axios.interceptors.response.use(undefined, function (error) {
  if (error) {
    const originalRequest = error.config
    if (error.response.status === 401 && !originalRequest._retry) {
      const userStore = useUserStore()
      originalRequest._retry = true
      userStore.logoutUser()
      return router.push('/login')
    }
  }
})

const app = createApp(App)
app.use(router)
app.use(pinia)
app.mount('#app')
