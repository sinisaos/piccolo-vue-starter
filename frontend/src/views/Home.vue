<template>
    <div>
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
            <nav aria-label="page navigation" v-if="tasks.length > 0">
                <ul class="pagination justify-content-center">
                    <li
                        class="page-item"
                        v-bind:class="{ disabled: page === 1 }"
                    >
                        <a
                            v-on:click.prevent="getTasks(page - 1)"
                            tabindex="-1"
                            class="page-link"
                            href=""
                            ><i class="fa fa-arrow-left" aria-hidden="true"></i
                        ></a>
                    </li>
                    <li class="page-item" :key="n" v-for="n in totalPages">
                        <a
                            v-bind:class="{ active: n === page }"
                            v-on:click.prevent="getTasks(n)"
                            class="page-link"
                            href=""
                            style="border-radius: 0em"
                            >{{ n }}</a
                        >
                    </li>
                    <li
                        class="page-item"
                        v-bind:class="{ disabled: page === totalPages }"
                    >
                        <a
                            v-on:click.prevent="getTasks(page + 1)"
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
import axios from "axios"
import dayjs from "dayjs"
import { defineComponent } from "vue"
import Footer from "../components/Footer.vue"

export default defineComponent({
    data() {
        return {
            tasks: [],
            page: 1,
            pageSize: 9,
            totalPages: 0
        }
    },
    components: {
        Footer
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
        async getTasks(pageNumber) {
            const totalResponse = await axios.get("/tasks/count/")
            this.totalPages = Math.ceil(
                totalResponse.data.count / this.pageSize
            )
            const response = await axios.get(
                `/tasks/?__page=${pageNumber}&__page_size=${this.pageSize}&__readable=true`
            )
            this.tasks = response.data.rows
            this.page = pageNumber
            return this.tasks
        }
    },
    mounted() {
        this.getTasks(this.page)
    }
})
</script>
