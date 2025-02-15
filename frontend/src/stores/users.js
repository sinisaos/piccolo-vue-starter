import axios from 'axios'
import { defineStore } from 'pinia'


export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    tasks: null,
  }),
  getters: {
    isAuthenticated: (state) => state.user,
  },
  actions: {
    async registerUser(form) {
      const response = await axios.post('accounts/register/', form)
      let userForm = new FormData()
      userForm.append('username', form.username)
      userForm.append('email', form.email)
      userForm.append('password', form.password)
      this.user = form.data
    },
    async loginUser(user) {
      const response = await axios.post('accounts/login/', user)
      console.log(response.data.error)
      this.user = response.data
    },
    async userProfile() {
      const response = await axios.get('accounts/profile/')
      this.user = response.data
    },
    async deleteUser() {
      await axios.delete(`accounts/delete/`)
      this.user = null
    },
    async logoutUser() {
      await axios.get('accounts/logout/')
      this.user = null
    },
    async userTasks() {
      const response = await axios.get('accounts/profile/tasks/')
      this.tasks = response.data
    },
  },
  persist: true,
})