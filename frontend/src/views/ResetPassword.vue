<template>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-lg-4 col-md-4 col-sm-4">
                <div v-if="!message" class="card">
                    <div class="card-title text-center">
                        <h3 class="p-3">Reset password</h3>
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
                                <label for="new_password" class="form-label"
                                    >New password:</label
                                >
                                <input
                                    type="password"
                                    name="new_password"
                                    v-model="newPassword"
                                    class="form-control"
                                    :class="{
                                        'is-invalid': v$.newPassword.$error
                                    }"
                                />
                                <div
                                    v-if="v$.newPassword.$error"
                                    class="invalid-feedback"
                                >
                                    <span v-if="!v$.newPassword.required"
                                        >Password is required</span
                                    >
                                    <span v-if="!v$.newPassword.minLength"
                                        >Password must be at least 6
                                        characters</span
                                    >
                                </div>
                            </div>
                            <div class="mb-3">
                                <label
                                    for="confirm_new_password"
                                    class="form-label"
                                    >Confirm new password:</label
                                >
                                <input
                                    type="password"
                                    name="confirm_new_password"
                                    v-model="passwordNewConfirmation"
                                    class="form-control"
                                    :class="{
                                        'is-invalid':
                                            v$.passwordNewConfirmation.$error
                                    }"
                                />
                                <div
                                    v-if="v$.passwordNewConfirmation.$error"
                                    class="invalid-feedback"
                                >
                                    <span
                                        v-if="
                                            !v$.passwordNewConfirmation.required
                                        "
                                        >Confirm Password is required</span
                                    >
                                    <span
                                        v-else-if="
                                            !v$.passwordNewConfirmation
                                                .sameAsPassword
                                        "
                                        >Passwords must match</span
                                    >
                                </div>
                            </div>
                            <div class="mb-3">
                                <label for="token" class="form-label"
                                    >Token:</label
                                >
                                <input
                                    type="text"
                                    name="token"
                                    v-model="token"
                                    class="form-control"
                                />
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
                            <router-link to="/login">Sign In</router-link>
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
import { required, minLength, sameAs } from "@vuelidate/validators"

export default defineComponent({
    setup() {
        return { v$: useVuelidate() }
    },
    data() {
        return {
            newPassword: "",
            passwordNewConfirmation: "",
            token: "",
            error: "",
            message: ""
        }
    },
    validations() {
        return {
            newPassword: { required, minLength: minLength(6) },
            passwordNewConfirmation: {
                required,
                sameAsPassword: sameAs(this.newPassword)
            }
        }
    },
    methods: {
        async submit() {
            const data = {
                new_password: this.newPassword,
                confirm_new_password: this.passwordNewConfirmation,
                token: this.token
            }
            try {
                this.v$.$touch()
                if (this.v$.$invalid) {
                    return
                }
                const response = await axios.post("reset-password/", data)
                this.message = response.data
            } catch (error) {
                this.error = true
            }
        }
    }
})
</script>

