<template>
    <div class="container">
        <div class="row row-cols-1 row-cols-md-3 g-2">
            <div v-for="task in tasks" :key="task.id">
                <div class="card p-2 mb-4 rounded">
                    <div class="card-body">
                        <p class="mb-0">
                            Posted by
                            <span
                                ><b>{{ task.task_user_readable }}</b>
                                <i>
                                    on {{ formatDate(task.created_at) }}</i
                                ></span
                            >
                        </p>
                        <h2>
                            {{ task.name }}
                        </h2>
                        <p class="mb-0">Completed - {{ task.completed }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import axios from "axios"
import dayjs from "dayjs"
import { defineComponent } from "vue"

export default defineComponent({
    data() {
        return {
            tasks: []
        }
    },
    computed: {
        isLoggedIn() {
            return this.$store.getters.isAuthenticated
        }
    },
    methods: {
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("MMMM D, YYYY")
        },
        async getTasks() {
            let response = await axios.get("/tasks/?__readable=true")
            this.tasks = response.data.rows
            return this.tasks
        }
    },
    mounted() {
        this.getTasks()
    }
})
</script>
