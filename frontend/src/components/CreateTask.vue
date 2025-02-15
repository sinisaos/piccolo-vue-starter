<template>
    <section>
        <button
            type="button"
            class="btn btn-success"
            v-on:click="isShow = !isShow"
            id="create-button"
        >
            Create task
        </button>
        <div v-if="isShow">
            <form @submit.prevent="submit">
                <div class="mb-3">
                    <label for="name" class="form-label">Name</label>
                    <input
                        type="text"
                        name="name"
                        v-model="name"
                        class="form-control"
                    />
                </div>
                <div class="mb-3">
                    <label for="completed" class="form-label">Completed</label>
                    <select class="form-select" v-model="completed">
                        <option value="false">False</option>
                        <option value="true">True</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="created" class="form-label">Created</label>
                    <VueDatePicker
                        input-class="form-control"
                        type="datetime"
                        v-model="created"
                        format="yyyy-MM-dd HH:mm"
                    ></VueDatePicker>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
            <br />
        </div>
    </section>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { useUserStore } from "../stores/users"
import { useTaskStore } from "../stores/tasks"
import VueDatePicker from "@vuepic/vue-datepicker"
import "@vuepic/vue-datepicker/dist/main.css"

export default defineComponent({
    setup() {
        const userStore = useUserStore()
        const taskStore = useTaskStore()
        return { userStore, taskStore }
    },
    data() {
        return {
            name: "",
            completed: "",
            created: "",
            taskUser: undefined,
            isShow: false
        }
    },
    components: {
        VueDatePicker
    },
    methods: {
        async submit() {
            let data = {
                name: this.name,
                completed: this.completed,
                created_at: this.created.toISOString().slice(0, -5),
                task_user: this.userStore.user.id
            }
            await this.taskStore.createTask(data)
            await this.userStore.userTasks()
            this.isShow = false
            this.name = this.completed = this.created = ""
        }
    }
})
</script>

<style scoped>
#create-button {
    margin-bottom: 1em;
}
</style>
