<template>
  <div style="padding:40px">
    <h1>Admin Dashboard</h1>

    <h3 v-if="user">
        Welcome {{ user.name }} </h3>

    <br><br>

    <div class="stats">

        <div class="card">
            <h2>{{ stats.students }}</h2>
            <p>Total Students</p>
        </div>

        <div class="card">
            <h2>{{ stats.companies }}</h2>
            <p>Total Companies</p>
        </div>

        <div class="card">
            <h2>{{ stats.jobs }}</h2>
            <p>Total Jobs</p>
        </div>

        <div class="card">
            <h2>{{ stats.applications }}</h2>
            <p>Total Applications</p>
        </div>

    </div>
    <br>
    <button @click="logout">Logout</button>
</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/app";

const router = useRouter();

const user = ref(null);
const stats = ref({
    students: 0,
    companies: 0,
    jobs: 0,
    applications: 0
});

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
    loadStats();
});
async function loadStats() {
    try {
        const response = await api.get("/admin/stats");
        stats.value = response.data;
    } catch (error) {
        console.log(error);
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    router.push("/");
}
</script>

<style scoped>

.stats{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:20px;
    margin-top:30px;
}

.card{
    background:#ffffff;
    border-radius:12px;
    padding:30px;
    text-align:center;
    box-shadow:0 2px 10px rgba(0,0,0,.15);
}

.card h2{
    font-size:40px;
    margin:0;
    color:#0d6efd;
}

.card p{
    margin-top:10px;
    font-size:18px;
}

button{
    margin-top:20px;
    padding:10px 20px;
    background:#dc3545;
    color:white;
    border:none;
    border-radius:6px;
    cursor:pointer;
}

button:hover{
    background:#bb2d3b;
}

</style>