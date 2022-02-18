<template>
    <div class="d-flex flex-column">
        <footer class="mt-auto py-3 bg-light" id="footer">
            <div class="container">
                <span class="text-muted"
                    >&copy; {{ new Date().getFullYear() }} Piccolo | Vue</span
                >
            </div>
        </footer>
    </div>
</template>

<script>
export default {}
</script>

<style scoped>
#footer {
    position: fixed;
    padding: 10px 10px 0px 10px;
    bottom: 0;
    width: 100%;
    height: 3em;
}
</style>

