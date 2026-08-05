<template>
  <div style="padding:40px">
    <h1>Admin Dashboard</h1>

    <h3 v-if="user">
      Welcome {{ user.name }}
    </h3>

    <p><b>Email:</b> {{ user?.email }}</p>
    <p><b>Role:</b> {{ user?.role }}</p>
    <p><b>ID:</b> {{ user?.id }}</p>

    <button @click="logout">Logout</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/app";

const router = useRouter();

const user = ref(null);

async function loadUser() {
    try {
        const response = await api.get("/me");
        user.value = response.data;
        console.log(response.data);
    } catch (error) {
        console.log(error);
    }
}

onMounted(() => {
    loadUser();
});
function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    router.push("/");
}
</script>