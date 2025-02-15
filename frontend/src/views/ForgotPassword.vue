<template>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-lg-4 col-md-4 col-sm-4">
                <div v-if="!message" class="card">
                    <div class="card-title text-center">
                        <h3 class="p-3">Forgot Password</h3>
                        <div
                            v-if="error"
                            class="alert alert-warning"
                            role="alert"
                        >
                            Unable to send email
                        </div>
                    </div>
                    <div class="card-body">
                        <form @submit.prevent="submit">
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
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary">
                                    Submit
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
                <div v-else class="card">
                    <div class="alert alert-success" role="alert">
                        {{ message }}
                    </div>
                    <div
                        class="container d-flex align-items-center justify-content-center"
                    >
                        <p class="float-start">
                            <router-link to="reset-password"
                                >Reset Password</router-link
                            >
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import axios from "axios"
import { defineComponent } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, email } from "@vuelidate/validators"

export default defineComponent({
    setup() {
        return { v$: useVuelidate() }
    },
    data() {
        return {
            email: "",
            error: "",
            message: ""
        }
    },
    validations() {
        return {
            email: { required, email }
        }
    },
    methods: {
        async submit() {
            const data = {
                email: this.email
            }
            try {
                const response = await axios.post("forgot-password/", data)
                this.message = response.data
            } catch (error) {
                this.error = true
            }
        }
    }
})
</script>

