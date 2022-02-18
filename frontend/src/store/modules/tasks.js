import axios from 'axios'

const state = {
  tasks: undefined,
  task: undefined
}

const getters = {
  stateTasks: state => state.tasks,
  stateTask: state => state.task,
}

const actions = {
  async createTask(context, task) {
    await axios.post('tasks', task)
    context.dispatch('userTasks')
  },
  async getTasks(context) {
    const response = await axios.get('tasks')
    context.commit('setTasks', response.data.rows)
  },
  async singleTask(context, id) {
    const response = await axios.get(`tasks/${id}`)
    context.commit('setTask', response.data)
  },
  // eslint-disable-next-line no-empty-pattern
  async updateTask({ }, task) {
    await axios.patch(`tasks/${task.id}`, task.form)
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteTask({ }, id) {
    console.log(id)
    await axios.delete(`tasks/${id}`)
  }
}

const mutations = {
  setTasks(state, tasks) {
    state.tasks = tasks
  },
  setTask(state, task) {
    state.task = task
  },
};

export default {
  state,
  getters,
  actions,
  mutations
}
