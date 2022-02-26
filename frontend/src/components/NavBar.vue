<template>
    <header>
        <nav class="navbar navbar-expand-md navbar-light bg-light">
            <div class="container">
                <router-link class="navbar-brand" to="/"
                    >Piccolo | Vue</router-link
                >
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
                        v-if="isAuthenticated"
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
                                Hello {{ stateUser.username }}
                            </a>
                            <ul
                                class="dropdown-menu"
                                aria-labelledby="navbarDropdown"
                            >
                                <li>
                                    <router-link
                                        class="dropdown-item"
                                        to="/profile"
                                        >Profile</router-link
                                    >
                                </li>
                                <li>
                                    <a class="dropdown-item" v-on:click="logout"
                                        >Logout</a
                                    >
                                </li>
                            </ul>
                        </li>
                    </ul>
                    <ul v-else class="navbar-nav ms-auto mb-2 mb-md-0">
                        <li class="nav-item">
                            <router-link class="nav-link" to="/login"
                                >Log In</router-link
                            >
                        </li>
                        <li class="nav-item">
                            <router-link class="nav-link" to="/register"
                                >Register</router-link
                            >
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>
</template>

<script>
import { mapGetters } from "vuex"

export default {
    computed: {
        ...mapGetters(["isAuthenticated", "stateUser"])
    },
    methods: {
        async logout() {
            await this.$store.dispatch("logoutUser")
            this.$router.push("/")
        }
    },
    watch: {
        $route() {
            document.querySelector("#navbarScroll").classList.remove("show")
        }
    }
}
</script>

<style scoped>
a {
    cursor: pointer;
}
</style>
