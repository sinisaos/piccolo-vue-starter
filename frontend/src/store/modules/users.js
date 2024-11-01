import axios from 'axios'

const state = {
  user: undefined,
  tasks: undefined,
}

const getters = {
  isAuthenticated: state => !!state.user,
  stateUser: state => state.user,
}

const actions = {
  async registerUser(context, form) {
    const response = await axios.post('accounts/register', form)
    let userForm = new FormData()
    userForm.append('username', form.username)
    userForm.append('email', form.email)
    userForm.append('password', form.password)
    context.commit('setUser', response.data)
    await context.dispatch('loginUser', userForm)
  },
  async loginUser(context, user) {
    const response = await axios.post('accounts/login', user)
    console.log(response.data.error)
    context.dispatch('userProfile', response.data)
  },
  async userProfile(context) {
    const response = await axios.get('accounts/profile/')
    context.commit('setUser', response.data)
  },
  async deleteUser() {
    await axios.delete(`accounts/delete/`)
  },
  async logoutUser(context) {
    await axios.get('accounts/logout/')
    context.commit('logout')
  },
  async userTasks(context) {
    const response = await axios.get('accounts/profile/tasks/')
    context.commit('setTasks', response.data)
  },
}

const mutations = {
  setUser(state, username) {
    state.user = username
  },
  logout(state, user) {
    state.user = user
  },
}

export default {
  state,
  getters,
  actions,
  mutations
}
