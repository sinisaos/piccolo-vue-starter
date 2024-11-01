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

<script>
import { mapGetters, mapActions } from "vuex"
import VueDatePicker from "@vuepic/vue-datepicker"
import "@vuepic/vue-datepicker/dist/main.css"

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
        VueDatePicker
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
                created_at: this.created.toISOString().slice(0, -5),
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

<style lang="less" scoped>
#create-button {
    margin-bottom: 1em;
}
</style>
