<template>
    <div class="container">
        <CreateTask />
        <div class="table-responsive">
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th scope="col">Id</th>
                        <th scope="col">Name</th>
                        <th scope="col">Completed</th>
                        <th scope="col">Created</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="task in tasks" :key="task.id">
                        <td>{{ task.id }}</td>
                        <td>{{ task.name }}</td>
                        <td>{{ task.completed }}</td>
                        <td>{{ task.created_at }}</td>
                        <td>
                            <router-link
                                :to="{
                                    name: 'EditTask',
                                    params: {
                                        id: task.id
                                    }
                                }"
                                class="btn btn-warning"
                            >
                                <i
                                    class="fa-regular fa-pen-to-square"
                                ></i></router-link
                            >&nbsp;
                            <button
                                class="btn btn-danger"
                                @click="removeTask(task.id)"
                            >
                                <i class="fa-regular fa-trash-can"></i>
                            </button>
                            <br />
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import { defineComponent } from "vue"
import { mapGetters, mapActions } from "vuex"
import CreateTask from "../components/CreateTask.vue"

export default defineComponent({
    components: {
        CreateTask
    },
    computed: {
        ...mapGetters({ user: "stateUser", tasks: "stateTasks" })
    },
    methods: {
        ...mapActions(["deleteTask"]),
        async removeTask(id) {
            if (confirm("Are you sure you want to delete this record!"))
                try {
                    await this.deleteTask(id)
                    this.$store.dispatch("userTasks")
                } catch (error) {
                    console.error(error)
                }
        }
    }
})
</script>
