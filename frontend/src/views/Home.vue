<template>
    <div class="container">
        <div v-for="task in tasks" :key="task.id">
            <div class="card shadow p-2 mb-4 rounded">
                <div class="card-body">
                    <p class="mb-0">
                        Posted by:
                        <span
                            ><b>{{ task.task_user_readable }}</b> at
                            {{ task.created_at }}</span
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
</template>
<script>
import axios from "axios"

export default {
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
        async getTasks() {
            let response = await axios.get("/tasks/?__readable=true")
            this.tasks = response.data.rows
            return this.tasks
        }
    },
    mounted() {
        this.getTasks()
    }
}
</script>
