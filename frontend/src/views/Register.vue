<template>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-lg-4 col-md-4 col-sm-4">
                <div class="card">
                    <div class="card-title text-center">
                        <h3 class="p-3">Sign Up</h3>
                        <div
                            v-if="error"
                            class="alert alert-danger"
                            role="alert"
                        >
                            User already exists. Please try again.
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
                                    :class="{
                                        'is-invalid': v$.username.$error
                                    }"
                                />
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label"
                                    >Email:</label
                                >
                                <input
                                    type="text"
                                    name="email"
                                    v-model="email"
                                    class="form-control"
                                    :class="{ 'is-invalid': v$.email.$error }"
                                />
                                <div
                                    v-if="v$.email.$error"
                                    class="invalid-feedback"
                                >
                                    <span v-if="!v$.email.required"
                                        >Email is required</span
                                    >
                                    <span v-if="!v$.email.email"
                                        >Email is invalid</span
                                    >
                                </div>
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
                                    :class="{
                                        'is-invalid': v$.password.$error
                                    }"
                                />
                                <div
                                    v-if="v$.password.$error"
                                    class="invalid-feedback"
                                >
                                    <span v-if="!v$.password.required"
                                        >Password is required</span
                                    >
                                    <span v-if="!v$.password.minLength"
                                        >Password must be at least 6
                                        characters</span
                                    >
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="confirm_password" class="form-label"
                                    >Confirm password:</label
                                >
                                <input
                                    type="password"
                                    name="password"
                                    v-model="passwordConfirmation"
                                    class="form-control"
                                    :class="{
                                        'is-invalid':
                                            v$.passwordConfirmation.$error
                                    }"
                                />
                                <div
                                    v-if="v$.passwordConfirmation.$error"
                                    class="invalid-feedback"
                                >
                                    <span
                                        v-if="!v$.passwordConfirmation.required"
                                        >Confirm Password is required</span
                                    >
                                    <span
                                        v-else-if="
                                            !v$.passwordConfirmation
                                                .sameAsPassword
                                        "
                                        >Passwords must match</span
                                    >
                                </div>
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
                                    Already have account?
                                    <router-link to="/login"
                                        >Sign In</router-link
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

<script lang="ts">
import { defineComponent } from "vue"
import { useUserStore } from "../stores/users"
import { useVuelidate } from "@vuelidate/core"
import { required, email, minLength, sameAs } from "@vuelidate/validators"

export default defineComponent({
    setup() {
        const userStore = useUserStore()
        return { userStore, v$: useVuelidate() }
    },
    data() {
        return {
            username: "",
            email: "",
            password: "",
            passwordConfirmation: "",
            error: ""
        }
    },
    validations() {
        return {
            username: { required },
            email: { required, email },
            password: { required, minLength: minLength(6) },
            passwordConfirmation: {
                required,
                sameAsPassword: sameAs(this.password)
            }
        }
    },
    methods: {
        async submit() {
            const data = {
                username: this.username,
                email: this.email,
                password: this.password
            }
            try {
                this.v$.$touch()
                if (this.v$.$invalid) {
                    return
                }
                await this.userStore.registerUser(data)
                this.$router.push("/login")
            } catch (error) {
                this.error = true
            }
        }
    }
})
</script>

