<template>
    <div class="container">
        <h2>Profile</h2>
        <ul class="list-group">
            <li
                class="list-group-item d-flex justify-content-between align-items-center"
            >
                <strong>Username</strong>
                <span>{{ user.username }}</span>
            </li>
            <li
                class="list-group-item d-flex justify-content-between align-items-center"
            >
                <strong>Email</strong>
                <span>{{ user.email }}</span>
            </li>
            <li
                class="list-group-item d-flex justify-content-between align-items-center"
            >
                <strong>Last login</strong>
                <span>{{ formatDate(user.last_login) }}</span>
            </li>
            <li
                class="list-group-item d-flex justify-content-between align-items-center"
            >
                <strong
                    ><router-link to="/dashboard">Tasks</router-link></strong
                >
                <span class="badge bg-primary rounded-pill">{{
                    tasks?.length
                }}</span>
            </li>
            <li
                class="list-group-item d-flex justify-content-between align-items-center"
            >
                <button v-on:click="deleteAccount()" class="btn btn-danger">
                    Delete Account
                </button>
            </li>
        </ul>
    </div>
</template>

<script>
import { defineComponent } from "vue"
import { mapGetters, mapActions } from "vuex"
import dayjs from "dayjs"

export default defineComponent({
    computed: {
        ...mapGetters({ user: "stateUser", tasks: "stateTasks" })
    },
    methods: {
        ...mapActions(["deleteUser"]),
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("MMMM D, YYYY")
        },
        async deleteAccount() {
            if (confirm("Are you sure you want to delete the account!"))
                try {
                    await this.deleteUser(this.user.id)
                    await this.$store.dispatch("logoutUser")
                    this.$router.push("/")
                } catch (error) {
                    console.error(error)
                }
        }
    },
    mounted() {
        this.$store.dispatch("userTasks")
        this.$store.dispatch("userProfile")
    }
})
</script>
