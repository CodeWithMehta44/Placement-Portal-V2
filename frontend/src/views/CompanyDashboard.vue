<template>
  <div style="padding:40px">

   <div class="dashboard-header">

    <div>
        <h1>Welcome, {{ companyName }}</h1>
        <p>Manage your placement drives from one place.</p>
    </div>

    <div class="header-buttons">

        <button
        class="profile-btn"
        @click="$router.push('/company/profile')"
        >
        Profile
        </button>

        <button class="logout-btn"  @click="logout">
            Logout
        </button>

    </div>

</div>

    <div class="stats-container">

      <div class="stat-card">
        <h2>{{ stats.totalJobs }}</h2>
        <p>Total Jobs</p>
      </div>

      <div class="stat-card">
        <h2>{{ stats.activeJobs }}</h2>
        <p>Active Jobs</p>
      </div>

      <div class="stat-card">
        <h2>{{ stats.applications }}</h2>
        <p>Applications</p>
      </div>

      <div class="stat-card">
        <h2>{{ stats.shortlisted }}</h2>
        <p>Shortlisted</p>
      </div>

    </div>

    <br>

    <div class="action-bar">
       <button
    class="create-btn"
    @click="$router.push('/company/create-job')"
>
    + Create New Job
</button>
        </div>

    <br><br>
    <table class="job-table">

      <h2 class="section-title">My Placement Drives</h2>

<div class="job-list">

    <div
        class="job-card"
        v-for="job in jobs"
        :key="job.id"
        >

        <div class="job-info"> 
            <div class="job-header">
                <div>

                    <h3>{{ job.title }}</h3>

                    <p class="company-name">
                        {{ companyName }}
                    </p>

                </div>

                <div
                    class="status-badge"
                    :class="job.is_active ? 'active' : 'closed'"
                >
                    {{ job.is_active ? "Active" : "Closed" }}
                </div>
        </div>
    </div>
       
    <div class="job-salary">
        <div class="job-details">
            <p>
                💰 ₹{{ (job.salary / 100000).toFixed(0) }} LPA
            </p>
            <p>
                📅 {{ job.deadline }}
            </p>
        </div>
    </div>
        

     <div class="job-actions">
         <button
             class="approve-btn"
             @click="$router.push(`/company/job/${job.id}/applications`)"
         >
             View Applicants
         </button>

        <button
             class="danger-btn"
             @click="toggleStatus(job)"
         >
             {{ job.is_active ? "Close Job" : "Open Job" }}
         </button>
     </div>

    </div>

</div>

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

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    router.push("/");
}
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

async function toggleStatus(job) {
    try {
        await api.put(`/company/job/${job.id}/status`, {
            is_active: !job.is_active
        });

        job.is_active = !job.is_active;

        alert("Job status updated successfully");
    } catch (error) {
        alert(error.response?.data?.error || "Something went wrong");
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
}

.dashboard-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:40px;
}

.dashboard-header h1{
    margin:0;
    font-size:42px;
}

.dashboard-header p{
    margin-top:8px;
    color:#666;
}

.header-buttons{
    display:flex;
    gap:15px;
}

.profile-btn{
    background:#0d6efd;
    color:white;
    border:none;
    padding:12px 22px;
    border-radius:8px;
    cursor:pointer;
}

.logout-btn{
    background:#dc3545;
    color:white;
    border:none;
    padding:12px 22px;
    border-radius:8px;
    cursor:pointer;
}

.stats-container{
    display:flex;
    gap:25px;
    margin:40px 0;
}

.stat-card{
    flex:1;
    background:white;
    border-radius:14px;
    padding:30px;
    text-align:center;
    box-shadow:0 4px 15px rgba(0,0,0,.08);
}

.stat-card h2{
    color:#198754;
    font-size:40px;
    margin:0;
}

.stat-card p{
    margin-top:12px;
    color:#666;
    font-weight:600;
}

.action-bar{
    margin:30px 0;
}

.section-title{
    margin:25px 0 15px;
}

.job-list{
    display:flex;
    flex-wrap:wrap;
    gap:20px;
    margin-top:20px;
}

.job-card{
    width:450px;
    background:white;
    border-radius:14px;
    padding:22px;
    box-shadow:0 4px 15px rgba(0,0,0,.08);

    display:flex;
    flex-direction:column;
    justify-content:space-between;

    transition:.3s;
}

.job-card:hover{
    transform:translateY(-5px);
    box-shadow:0 10px 25px rgba(0,0,0,.15);
}

.job-header{
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    margin-bottom:20px;
}

.job-header h3{
    margin:0;
    font-size:24px;
}

.company-name{
    margin-top:8px;
    color:#777;
}

.job-details{
    margin:12px 0;
    font-size:16px;
}

.job-details p{
    margin:10px 0;
    color:#555;
}

.job-info{
    flex:2;
}

.job-salary{
    flex:1;
    text-align:left;
}
.job-actions{
    display:flex;
    gap:10px;
    margin-top:18px;
}

.status-badge{
    padding:8px 16px;
    border-radius:20px;
    font-size:14px;
    font-weight:600;
}

.active{
    background:#d1fae5;
    color:#198754;
}

.closed{
    background:#fde2e2;
    color:#dc3545;
}
.approve-btn{
    width:100%;
    margin-top:20px;
    padding:12px;
    border:none;
    border-radius:8px;
    background:#198754;
    color:white;
    font-weight:bold;
    cursor:pointer;
    transition:.3s;
}

.approve-btn:hover{
    background:#157347;
}

.danger-btn{
    background:#dc3545;
    color:white;
    border:none;
    padding:10px 18px;
    border-radius:6px;
    cursor:pointer;
    margin-left:10px;
}

.danger-btn:hover{
    background:#bb2d3b;
}
</style>