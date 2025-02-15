<template>
    <div>
        <div class="container">
            <div class="row row-cols-1 row-cols-md-3 g-2">
                <div v-for="task in taskStore.tasks" :key="task.id">
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
            <nav
                aria-label="page navigation"
                v-if="taskStore.tasks?.length > 0"
            >
                <ul class="pagination justify-content-center">
                    <li
                        class="page-item"
                        v-bind:class="{ disabled: taskStore.page === 1 }"
                    >
                        <a
                            v-on:click.prevent="getAllTasks(taskStore.page - 1)"
                            tabindex="-1"
                            class="page-link"
                            href=""
                            ><i class="fa fa-arrow-left" aria-hidden="true"></i
                        ></a>
                    </li>
                    <li
                        class="page-item"
                        :key="n"
                        v-for="n in taskStore.totalPages"
                    >
                        <a
                            v-bind:class="{ active: n === taskStore.page }"
                            v-on:click.prevent="getAllTasks(n)"
                            class="page-link"
                            href=""
                            style="border-radius: 0em"
                            >{{ n }}</a
                        >
                    </li>
                    <li
                        class="page-item"
                        v-bind:class="{
                            disabled: taskStore.page === taskStore.totalPages
                        }"
                    >
                        <a
                            v-on:click.prevent="getAllTasks(taskStore.page + 1)"
                            class="page-link"
                            href=""
                            ><i class="fa fa-arrow-right" aria-hidden="true"></i
                        ></a>
                    </li>
                </ul>
            </nav>
        </div>
        <Footer />
    </div>
</template>
<script>
import { defineComponent } from "vue"
import { useTaskStore } from "../stores/tasks"
import dayjs from "dayjs"
import Footer from "../components/Footer.vue"

export default defineComponent({
    setup() {
        const taskStore = useTaskStore()
        return { taskStore }
    },
    components: {
        Footer
    },
    methods: {
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("MMMM D, YYYY")
        },
        async getAllTasks(pageNumber) {
            await this.taskStore.getTasks(pageNumber)
        }
    },
    async mounted() {
        await this.getAllTasks(this.taskStore.page)
    }
})
</script>
