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
            <form ref="anyName" @submit.prevent="submit">
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
                    <datetime
                        input-class="form-control"
                        type="datetime"
                        v-model="created"
                        format="yyyy-dd-MM HH:mm"
                    ></datetime>
                </div>
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
            <br />
        </div>
    </section>
</template>

<script>
import { mapGetters, mapActions } from "vuex"
import { Datetime } from "vue-datetime"
import "vue-datetime/dist/vue-datetime.css"

export default {
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
        datetime: Datetime
    },
    computed: {
        ...mapGetters({ user: "stateUser", tasks: "stateTasks" })
    },
    methods: {
        ...mapActions(["createTask"]),
        async submit() {
            let data = {
                name: this.name,
                completed: this.completed,
                created_at: this.created.slice(0, -5),
                task_user: this.user.id
            }
            await this.createTask(data)
            this.$store.dispatch("userTasks")
            this.isShow = false
            this.name = this.completed = this.created = ""
        }
    }
}
</script>

<style scoped>
#create-button {
    margin-bottom: 1em;
}
</style>
