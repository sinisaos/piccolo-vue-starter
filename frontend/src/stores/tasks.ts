import axios from 'axios'
import { defineStore } from 'pinia'


export const useTaskStore = defineStore('task', {
  state: () => ({
    tasks: null,
    task: null,
    page: 1,
    pageSize: 15,
    totalPages: 0
  }),
  actions: {
    async createTask(task: any) {
      const response = await axios.post('tasks', task)
      this.task = response.data
    },
    async getTasks(pageNumber: number) {
      const totalResponse = await axios.get("tasks/count/")
      this.totalPages = Math.ceil(
        totalResponse.data.count / this.pageSize
      )
      const response = await axios.get(
        `tasks/?__page=${pageNumber}&__page_size=${this.pageSize}&__readable=true`
      )
      this.tasks = response.data.rows
      this.page = pageNumber
    },
    async singleTask(id: Number) {
      const response = await axios.get(`tasks/${id}/`)
      this.task = response.data
    },
    async updateTask(task: { id: any; form: any }) {
      const response = await axios.patch(`tasks/${task.id}/`, task.form)
      this.task = response.data
    },
    async deleteTask(id: any) {
      await axios.delete(`tasks/${id}/`)
      this.task = null
    }
  },
})
