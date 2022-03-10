<template>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-lg-4 col-md-4 col-sm-4">
                <div class="card">
                    <div class="card-title text-center">
                        <h2 class="p-3">Login</h2>
                        <div
                            v-if="error"
                            class="alert alert-danger"
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
                            <button type="submit" class="btn btn-primary">
                                Submit
                            </button>
                            <p class="float-end">
                                Don't have account
                                <router-link to="/register"
                                    >Sign Up</router-link
                                >
                            </p>
                        </form>
                        <div class="card-title text-center">
                            <br />
                            <div class="seperator">
                                <hr />
                                <b>OR</b>
                            </div>
                            <GoogleLogin
                                class="btn btn-google"
                                :params="params"
                                :renderParams="renderParams"
                                :onSuccess="onSuccess"
                            ></GoogleLogin>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions } from "vuex"
import GoogleLogin from "vue-google-login"

export default {
    data() {
        return {
            username: "",
            password: "",
            error: false,
            params: {
                client_id: process.env.VUE_APP_CLIENT_ID
            },
            renderParams: {
                width: 260,
                height: 50,
                longtitle: true
            }
        }
    },
    components: {
        GoogleLogin
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
        },
        onSuccess(googleUser) {
            // data for register Google user as BaseUser with fake password
            // to satisfy Pydantic validation on backend
            let password = "0425346c32c9c3dd"
            let userInfo = {
                username: googleUser.getBasicProfile().getName(),
                email: googleUser.getBasicProfile().getEmail(),
                password: password
            }
            // form for login Google user as BaseUser with fake password because
            // we don't need a password when using a Google login. We can reveal
            // this password because is hashed by Piccolo backend anyway,
            // and we actually aren’t use this password. With this way both
            // username/password login and Google login can work together
            let loginForm = new FormData()
            loginForm.append("username", googleUser.getBasicProfile().getName())
            loginForm.append("password", password)
            this.$store
                .dispatch("registerUser", userInfo)
                .then(() => {
                    this.$router.push("/")
                })
                .catch(() => {
                    this.$store.dispatch("loginUser", loginForm)
                    this.$router.push("/")
                })
        }
    }
}
</script>

<style lang="less" scoped>
.seperator b {
    width: 40px;
    height: 40px;
    font-size: 16px;
    text-align: center;
    line-height: 40px;
    background: #fff;
    display: inline-block;
    border: 1px solid #e0e0e0;
    border-radius: 50%;
    position: relative;
    top: -36px;
    z-index: 1;
    margin-bottom: -1rem;
}
.float-end {
    padding-top: 0.5rem;
}
</style>