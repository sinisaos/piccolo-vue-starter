<template>
    <div id="app">
        <NavBar />
        <div class="main">
            <RouterView />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import NavBar from "./components/NavBar.vue"

export default defineComponent({
    components: {
        NavBar
    }
})
</script>

<style>
.main {
    padding-top: 1.5em;
}
</style>
