<template>
    <div class="container">
        <div class="row">
            <h2>Edit task</h2>
            <hr />
            <div v-if="taskStore.task">
                <form @submit.prevent="submit">
                    <label for="name" class="form-label">Name</label>
                    <input
                        type="text"
                        name="name"
                        v-model="form.name"
                        class="form-control"
                    />

                    <div class="mb-3">
                        <label for="completed" class="form-label"
                            >Completed</label
                        >
                        <select class="form-select" v-model="form.completed">
                            <option value="false">False</option>
                            <option value="true">True</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        Submit
                    </button>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { useTaskStore } from "../stores/tasks"

export default defineComponent({
    setup() {
        const taskStore = useTaskStore()
        return { taskStore }
    },
    props: {
        id: String
    },
    data() {
        return {
            form: {
                name: "",
                completed: ""
            }
        }
    },
    methods: {
        async submit() {
            let data = {
                id: this.id,
                form: this.form
            }
            try {
                await this.taskStore.updateTask(data)
                this.$router.push("/dashboard")
            } catch (error) {
                console.log(error)
            }
        },
        async getTask() {
            try {
                await this.taskStore.singleTask(this.id)
                this.form.name = this.taskStore.task.name
                this.form.completed = this.taskStore.task.completed
            } catch (error) {
                console.log(error)
            }
        }
    },
    async mounted() {
        await this.getTask()
    }
})
</script>
