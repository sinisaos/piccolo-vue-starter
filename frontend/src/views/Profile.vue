<template>
    <div class="container">
        <h2>Profile</h2>
        <ul class="list-group">
            <li
                class="list-group-item d-flex justify-content-between align-items-center"
            >
                <strong>Username</strong>
                <span>{{ userStore.user?.username }}</span>
            </li>
            <li
                class="list-group-item d-flex justify-content-between align-items-center"
            >
                <strong>Email</strong>
                <span>{{ userStore.user?.email }}</span>
            </li>
            <li
                class="list-group-item d-flex justify-content-between align-items-center"
            >
                <strong>Last login</strong>
                <span>{{ formatDate(userStore.user?.last_login) }}</span>
            </li>
            <li
                class="list-group-item d-flex justify-content-between align-items-center"
            >
                <strong
                    ><router-link to="/dashboard">Tasks</router-link></strong
                >
                <span class="badge bg-primary rounded-pill">{{
                    userStore.tasks?.length
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
import { useUserStore } from "../stores/users"
import dayjs from "dayjs"

export default defineComponent({
    setup() {
        const userStore = useUserStore()
        return { userStore }
    },
    methods: {
        formatDate(dateString) {
            const date = dayjs(dateString)
            return date.format("MMMM D, YYYY")
        },
        async deleteAccount() {
            if (confirm("Are you sure you want to delete the account!"))
                try {
                    await this.userStore.deleteUser(this.userStore.user.id)
                    await this.userStore.logoutUser()
                    this.$router.push("/")
                } catch (error) {
                    console.error(error)
                }
        }
    },
    async mounted() {
        await this.userStore.userTasks()
        await this.userStore.userProfile()
    }
})
</script>
