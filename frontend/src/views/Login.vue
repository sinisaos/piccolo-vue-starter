<template>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-lg-4 col-md-4 col-sm-4">
                <div class="card">
                    <div class="card-title text-center">
                        <h2 class="p-3">Sign In</h2>
                        <div
                            v-if="error"
                            class="alert alert-warning"
                            role="alert"
                        >
                            Incorrect username or password
                        </div>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="submit">
                            <div class="mb-3">
                                <label for="username" class="form-label"
                                    >Username:</label
                                >
                                <input
                                    type="text"
                                    name="username"
                                    v-model="username"
                                    class="form-control"
                                />
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label"
                                    >Password:</label
                                >
                                <input
                                    type="password"
                                    name="password"
                                    v-model="password"
                                    class="form-control"
                                />
                            </div>
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary">
                                    Submit
                                </button>
                            </div>
                            <br />
                            <div
                                class="container d-flex align-items-center justify-content-center"
                            >
                                <p>
                                    Don't have account?
                                    <router-link to="/register"
                                        >Sign Up</router-link
                                    >
                                </p>
                            </div>
                            <div
                                class="container d-flex align-items-center justify-content-center"
                            >
                                <p class="float-start">
                                    <router-link to="/forgot-password"
                                        >Forgot Password?</router-link
                                    >
                                </p>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent } from "vue"
import { mapActions } from "vuex"

export default defineComponent({
    data() {
        return {
            username: "",
            password: "",
            error: false
        }
    },
    methods: {
        ...mapActions(["loginUser", "registerUser"]),
        async submit() {
            const form = new FormData()
            form.append("username", this.username)
            form.append("password", this.password)
            await this.$store
                .dispatch("loginUser", form)
                .then(() => {
                    this.$router.push("/")
                })
                .catch(() => {
                    this.error = true
                })
        }
    }
})
</script>