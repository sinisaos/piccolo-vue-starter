<template>
    <header>
        <nav class="navbar navbar-expand-sm">
            <div class="container">
                <router-link class="navbar-brand" to="/"
                    >Piccolo | Vue</router-link
                >
                <ul class="navbar-nav ms-auto">
                    <button class="btn btn" id="themeSwitch">
                        <i
                            :class="
                                theme == 'dark'
                                    ? 'fa-regular fa-moon fa-xl'
                                    : 'fa-regular fa-sun fa-xl'
                            "
                        ></i>
                    </button>
                </ul>
                <button
                    class="navbar-toggler"
                    type="button"
                    data-bs-toggle="collapse"
                    data-bs-target="#navbarScroll"
                    aria-controls="navbarScroll"
                    aria-expanded="false"
                    aria-label="Toggle navigation"
                >
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarScroll">
                    <ul
                        v-if="userStore.isAuthenticated"
                        class="navbar-nav ms-auto mb-2 mb-md-0"
                    >
                        <li class="nav-item dropdown">
                            <a
                                class="nav-link dropdown-toggle"
                                href="#"
                                id="navbarDropdown"
                                role="button"
                                data-bs-toggle="dropdown"
                                aria-expanded="false"
                            >
                                <i class="fa-regular fa-circle-user"></i>
                                {{ userStore.user?.username }}
                            </a>
                            <ul
                                class="dropdown-menu"
                                aria-labelledby="navbarDropdown"
                            >
                                <li>
                                    <router-link
                                        class="dropdown-item"
                                        to="/profile"
                                        ><i class="fa-regular fa-user"></i>
                                        Profile</router-link
                                    >
                                </li>
                                <li>
                                    <a
                                        class="dropdown-item"
                                        v-on:click="logout"
                                        style="cursor: pointer"
                                        ><i
                                            class="fa fa-power-off"
                                            aria-hidden="true"
                                        ></i>
                                        Logout</a
                                    >
                                </li>
                            </ul>
                        </li>
                    </ul>
                    <ul v-else class="navbar-nav ms-auto mb-2 mb-md-0">
                        <li class="nav-item">
                            <router-link class="nav-link" to="/login"
                                >Sign In</router-link
                            >
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/register"
                                >Sign Up</router-link
                            >
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import { useUserStore } from "../stores/users"

export default defineComponent({
    setup() {
        const userStore = useUserStore()
        return { userStore }
    },
    data() {
        return {
            theme: ""
        }
    },
    methods: {
        async logout() {
            await this.userStore
                .logoutUser()
                .then(() => {
                    this.$router.push("/")
                })
                .catch(() => {
                    this.error = true
                })
        }
    },
    watch: {
        $route() {
            document.querySelector("#navbarScroll").classList.remove("show")
        }
    },
    mounted() {
        document.getElementById("themeSwitch").addEventListener("click", () => {
            if (
                document.documentElement.getAttribute("data-bs-theme") == "dark"
            ) {
                document.documentElement.setAttribute("data-bs-theme", "light")
                this.theme = "dark"
            } else {
                document.documentElement.setAttribute("data-bs-theme", "dark")
                this.theme = "true"
            }
        })
    }
})
</script>