<template>
  <div>
    <div class="dashboard-header">
    <div>
        <h1>
            Welcome,
            {{ student?.full_name || student?.name || "Student" }}
        </h1>
        <p>Manage your placement journey from one place.</p>
        
    </div>

    <div class="header-buttons">
        <button
            class="profile-btn"
            @click="router.push('/student/profile')"
        >
            Profile
        </button>

        <button
        class="logout-btn"
        @click="logout"
    >
        Logout
</button>
    </div>
</div>

<div class="stats-container">

    <div class="stat-card">
        <h3>{{ jobs.length }}</h3>
        <p>Available Jobs</p>
    </div>

    <div class="stat-card">
        <h3>{{ applications.length }}</h3>
        <p>Applications</p>
    </div>

    <div class="stat-card">
        <h3>
            {{ applications.filter(app => app.status === "Applied").length }}
        </h3>
        <p>Pending</p>
    </div>

</div>

<h1 class="notification-title">
    Notifications
</h1>

<div
    v-for="notification in notifications"
    :key="notification.id"
    class="interview-card"
>
    <h3>{{ notification.title }}</h3>

    <p>{{ notification.message }}</p>

    <small>{{ notification.created_at }}</small>

  <div
    v-if="applications.status === 'Interview'"
    class="interview-card"
  >
    <h3>📢 Interview Scheduled</h3>

    <p><strong>🏢 Company:</strong> {{ application.company }}</p>

    <p><strong>💼 Role:</strong> {{ application.title }}</p>

    <p><strong>📅 Date:</strong> {{ application.interview_date }}</p>

    <p><strong>🕒 Time:</strong> {{ application.interview_time }}</p>

    <p><strong>📍 Location:</strong> {{ application.interview_location }}</p>

    <p class="good-luck">
      Best of luck for your interview! 
    </p>
  </div>
</div>

<h2 class="section-title">Available Jobs</h2>

<div class="search-box">
  <input
    v-model="search"
    @input="loadJobs"
    type="text"
    placeholder="Search by company, title, skills..."
  />
</div>
  <div class="job-list">

   <div
    class="job-card"
    v-for="job in jobs"
    :key="job.id"
>
    <div class="job-header">

        <div>
            <h3>{{ job.title }}</h3>
            <p class="company-name">
                {{ job.company }}
            </p>
        </div>
        <div class="salary">
            ₹{{ (job.salary / 100000).toFixed(0) }} LPA
        </div>
    </div>
 

        <div class="job-info">

        <span>📍 {{ job.location }}</span>

        <span>📅 {{ job.deadline }}</span>
    </div>

    <button
        class="approve-btn"
        @click="$router.push(`/student/job/${job.id}`)"
    >
        View Details
    </button>

</div>

</div>
<h2 style="margin-top:50px;">
    My Applications
</h2>
<p v-if="applications.length === 0">
    No applications yet.
</p>
<table  v-else
    class="company-table"
>

    <thead>
        <tr>
            <th>Company</th>
            <th>Job Title</th>
            <th>Status</th>
            <th>Applied Date</th>
            <th>Action</th>
        </tr>
    </thead>

    <tbody>


        <tr
            v-for="application in applications"
            :key="application.id"
        >

            <td>{{ application.company }}</td>

            <td>{{ application.title }}</td>

            <td>
            <span class="status-badge">
                {{ application.status }}
            </span>
        </td>

            <td>{{ application.applied_date.split(" ")[0]  }}</td>

              <td>
        <button
            class="approve-btn"
            @click="$router.push(`/student/job/${application.job_id}`)"
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
import { ref, onMounted } from "vue";
import api from "../services/app";
import { useRouter } from "vue-router";

const jobs = ref([]);
const applications = ref([]);
const router = useRouter();
const student = ref({})
const notifications = ref([]);
const search = ref("")

function viewJob(id) {

    router.push(`/student/job/${id}`);

}

async function loadApplications() {

    try {

        const response = await api.get("/student/applications");

        applications.value = response.data;

    } catch (error) {

        console.log(error);

    }

}

async function loadNotifications() {
  try {
    const response = await api.get("/student/notifications");
    notifications.value = response.data;
  } catch (error) {
    console.log(error);
  }
}

async function loadStudent() {
    try {
        const res = await api.get("/student/profile")
        student.value = res.data
    } catch (err) {
        console.log(err)
    }
}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("user");

    router.push("/");
}

async function loadJobs() {
    try {
        const response = await api.get(
            `/student/jobs?search=${search.value}`
        );

        jobs.value = response.data;
    } catch (error) {
        console.log(error);
    }
}

onMounted(() => {

    loadJobs();
    loadApplications();
    loadStudent();
    loadNotifications();
});
</script>

<style scoped>
div{
    padding:15px;
}
.company-table{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
    background:white;
    border-radius:10px;
    overflow:hidden;
    box-shadow:0 2px 10px rgba(0,0,0,.15);
}

.company-table th{
    background: grey;
    color:white;
    padding:15px;
    text-align:left;
}

.company-table td{
    padding:15px;
    border-bottom:1px solid #ddd;
}

.company-table tr:hover{
    background:#f8f9fa;
}

.approve-btn{
    width:100%;
    padding:12px;
    border:none;
    border-radius:10px;
    background:#198754;
    color:white;
    font-size:15px;
    font-weight:600;
    cursor:pointer;
    transition:.3s;
}

.approve-btn:hover{
    background:#146c43;
}

.applied{
    color:#198754;
    font-weight:bold;
}

.shortlisted{
    color:#ffc107;
    font-weight:bold;
}

.rejected{
    color:#dc3545;
    font-weight:bold;
}
.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 24px 28px;
    margin-bottom: 25px;
    background: linear-gradient(135deg, #ffffff, #f3faf7);
    border-left: 5px solid #198754;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.dashboard-header h1 {
    margin: 0 0 6px 0;
    padding: 18px 28px;
    margin-bottom: 25px;
    font-size: 28px;
    font-weight: 700;
    color: #222;
}

.dashboard-header h1::first-letter {
    color: #198754;
    font-size: 26px;
    margin-bottom: 4px;
}

.dashboard-header p {
    margin: 0;
    color: #777;
    font-size: 14px;
}

.header-buttons {
    display: flex;
    gap: 10px;
}

.profile-btn,
.logout-btn {
    padding: 9px 18px;
    border: none;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    transition: 0.2s ease;
}

.profile-btn {
    background: #0d6efd;
    color: white;
}

.profile-btn:hover {
    background: #0b5ed7;
    transform: translateY(-1px);
}

.logout-btn {
    background: #dc3545;
    color: white;
}

.logout-btn:hover {
    background: #bb2d3b;
    transform: translateY(-1px);
}

.section-title{
    margin-bottom:20px;
}
.stats-container{
    display:flex;
    gap:25px;
    margin:35px 0;
}

.stat-card{
    flex:1;
    transform:translateY(-4px);
    background:white;
    border-radius:12px;
    padding:25px;
    text-align:center;
    box-shadow:0 2px 10px rgba(0,0,0,.1);
    transition:.3s;
}

.stat-card h3{
    font-size:35px;
    color:#198754;
    margin-bottom:10px;
}

.stat-card p{
    color:#666;
    font-weight:600;
}
.status-badge{
    background:#d1fae5;
    color:#198754;
    padding:6px 12px;
    border-radius:20px;
    font-weight:bold;
    font-size:14px;
}
.job-list{
    display:flex;
    flex-wrap:wrap;
    gap:25px;
    margin-top:20px;
    grid-template-columns:repeat(auto-fill,minmax(320px,1fr));
}
.job-card{
    width: 360px;
    background:white;
    border-radius:16px;
    padding:20px;
    border:1px solid #e9ecef;
    box-shadow:0 4px 15px rgba(0,0,0,.08);
    transition:.3s;
}
.job-card:hover{
    transform:translateY(-6px);
    border-color:#198754;
    box-shadow:0 15px 35px rgba(25,135,84,.15);
}

.job-header{
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    margin-bottom:20px;
}

.job-header h3{
    margin:0;
    font-size:22px;
}


.company-name{
    color:#6c757d;
    font-size:15px;
    margin-top:8px;
}

.salary{
    color:#198754;
    font-size:24px;
    font-weight:700;
    background:#e8f5ee;
    padding:8px 14px;
    border-radius:30px;
}

.job-info{
    display:flex;
    justify-content:space-between;
    margin:25px 0;
    color:#666;
    font-size:15px;
}

.interview-card{
    max-width: 600px;
    max-width: 90%;
    margin: 30px auto;
    padding: 24px;

    background:#f1fff6;
    border-left:6px solid #198754;
    border-radius:12px;
    box-shadow:0 8px 25px rgba(0,0,0,.08);
}

.interview-card h3{
    color:#198754;
    margin-bottom:18px;
}

.interview-card p{
    margin:10px 0;
    font-size:16px;
}

.good-luck{
    margin-top:15px;
    color:#198754;
    font-weight:bold;
}
.notification-title{
    margin-top:40px;
    margin-bottom:15px;
}

.search-box {
    margin: 20px 0;
    width: 50%;
}

.search-box input {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid #ddd;
    border-radius: 10px;
    font-size: 14px;
    outline: none;
    transition: all 0.2s ease;
    box-sizing: border-box;
    background: #fff;
}

.search-box input::placeholder {
    color: #999;
}

.search-box input:focus {
    border-color: #198754;
    box-shadow: 0 0 0 3px rgba(25, 135, 84, 0.12);
}

</style>