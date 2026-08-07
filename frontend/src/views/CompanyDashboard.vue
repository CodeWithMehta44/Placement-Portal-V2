<template>
  <div style="padding:40px">

    <h1>Company Dashboard</h1>

    <h3>Welcome {{ companyName }}</h3>

    <br>

    <div class="stats">

      <div class="card">
        <h2>{{ stats.totalJobs }}</h2>
        <p>Total Jobs</p>
      </div>

      <div class="card">
        <h2>{{ stats.activeJobs }}</h2>
        <p>Active Jobs</p>
      </div>

      <div class="card">
        <h2>{{ stats.applications }}</h2>
        <p>Applications</p>
      </div>

      <div class="card">
        <h2>{{ stats.shortlisted }}</h2>
        <p>Shortlisted</p>
      </div>

    </div>

    <br>

    <button class="create-btn">
      + Create Job
    </button>

    <br><br>

    <h2>My Jobs</h2>

    <table class="job-table">

      <thead>

      <tr>
        <th>Title</th>
        <th>Salary</th>
        <th>Deadline</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>

      </thead>

        <tbody>
        <tr v-for="job in jobs" :key="job.id">

            <td>{{ job.title }}</td>

            <td>₹ {{ job.salary }}</td>

            <td>{{ job.deadline }}</td>

            <td>
                <span v-if="job.is_active" style="color:green;">
                    Active
                </span>

                <span v-else style="color:red;">
                    Closed
                </span>
            </td>

            <td>
                <button
                    class="approve-btn"
                    @click="viewJob(job.id)"
                >
                    View
                </button>
            </td>

        </tr>
    </tbody>

    </table>

  </div>
</template>

<script setup>
import { ref } from "vue";
import { onMounted } from "vue";
import api from "../services/app";
import { useRouter } from "vue-router";

const companyName = ref("");
const jobs = ref([]);
const router = useRouter();

onMounted(() => {
    loadCompany();
    loadStats();
    loadJobs();
});

function viewJob(id) {
    router.push(`/company/job/${id}`);
}

async function loadCompany() {
    try {
        const response = await api.get("/me");
        companyName.value = response.data.name;
    } catch (error) {
        console.log(error);
    }
}

async function loadStats() {
    try {
        const response = await api.get("/company/stats");
        stats.value = response.data;
    } catch (error) {
        console.log(error);
    }
}

async function loadJobs() {
    try {
        const response = await api.get("/company/jobs");
        jobs.value = response.data;
    } catch (error) {
        console.log(error);
    }
}

const stats = ref({
    totalJobs:0,
    activeJobs:0,
    applications:0,
    shortlisted:0
});
</script>

<style>.stats{
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:20px;
    margin-top:30px;
}

.card{
    background:white;
    border-radius:12px;
    padding:30px;
    text-align:center;
    box-shadow:0 2px 10px rgba(0,0,0,.15);
}

.card h2{
    font-size:40px;
    color:#0d6efd;
    margin:0;
}

.card p{
    margin-top:10px;
}

.job-table{
    width:100%;
    border-collapse:collapse;
    background:white;
    border-radius:10px;
    overflow:hidden;
    box-shadow:0 2px 10px rgba(0,0,0,.15);
}

.job-table th{
    background:grey;
    color:white;
    padding:15px;
}

.job-table td{
    padding:15px;
    border-bottom:1px solid #ddd;
}

.create-btn{
    background:#198754;
    color:white;
    padding:10px 20px;
    border:none;
    border-radius:6px;
    cursor:pointer;
}

.create-btn:hover{
    background:#157347;
}</style>