<template>
  <div style="padding:40px">
    <h1>Admin Dashboard</h1>

    <h3 v-if="user">
        Welcome {{ user.name }} </h3>

        <button @click="logout">Logout</button>
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
        <p>Total Jobs Loaded: {{ jobs.length }}</p>
        <p>Total Applications Loaded: {{ applications.length }}</p>

    </div>

    <h2>Company Management</h2>

<table class="company-table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Company</th>
            <th>Industry</th>
            <th>Location</th>
            <th>Approval</th>
            <th>Account</th>
            <th>Actions</th>
        </tr>
    </thead>

    <tbody>
    <tr v-for="company in companies" :key="company.id">
         <td>{{ company.id }}</td>
         <td>{{ company.company_name }}</td>
         <td>{{ company.industry }}</td>
         <td>{{ company.location }}</td>
         <td>
            <span v-if="company.is_approved" style="color:green;">
                Approved
            </span>

            <span v-else style="color:red;">
                Pending
            </span>
        </td>

        <td>
            <span v-if="company.is_active" style="color:green;">
                Active
            </span>

            <span v-else style="color:red;">
                Inactive
            </span>
        </td>

        <td>
            <button
                v-if="!company.is_approved"
                class="approve-btn"
                @click="approveCompany(company.id)"
            >
                Approve
            </button>

            <button
                v-if="company.is_active"
                class="deactivate-btn"
                @click="deactivateCompany(company.id)"
            >
                Deactivate
            </button>

            <button
                v-else
                class="success-btn"
                @click="activateCompany(company.id)"
            >
                Activate
            </button>
        </td>
        </tr>
    </tbody>
</table>

<br><br>

<h2>Student Management</h2>

<table class="company-table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Course</th>
            <th>Resume</th>
            <th>Actions</th>
        </tr>
    </thead>

    <tbody>
        <tr v-for="student in students" :key="student.id">
            <td>{{ student.id }}</td>
            <td>{{ student.full_name }}</td>
            <td>{{ student.email }}</td>
            <td>{{ student.course }}</td>

            <td>
                <a
                    v-if="student.resume_url"
                    :href="student.resume_url"
                    target="_blank"
                >
                    View Resume
                </a>

                <span v-else>
                    Not Uploaded
                </span>
            </td>

            <td>
                <button
                    v-if="student.is_active"
                    @click="deactivateStudent(student.id)"
                    class="deactivate-btn"
                >
                    Deactivate
                </button>

                <button
                    v-else
                    @click="activateStudent(student.id)"
                    class="success-btn"
                >
                    Activate
                </button>
            </td>
        </tr>
    </tbody>
</table>

<br><br>

<h2>Job Management</h2>

<table class="company-table">
    <thead>
        <tr>
            <th>ID</th>
            <th>Job Title</th>
            <th>Company ID</th>
            <th>Location</th>
            <th>Salary</th>
            <th>Vacancies</th>
            <th>Deadline</th>
            <th>Actions</th>
        </tr>
    </thead>

    <tbody>
        <tr v-for="job in jobs" :key="job.id">

            <td>{{ job.id }}</td>
            <td>{{ job.title }}</td>
            <td>{{ job.company_id }}</td>
            <td>{{ job.location }}</td>
            <td>₹ {{ job.salary }}</td>
            <td>{{ job.vacancies }}</td>
            <td>{{ job.deadline }}</td>

            <td>
                <button
                    class="deactivate-btn"
                    @click="deleteJob(job.id)"
                >
                    Delete
                </button>
            </td>

        </tr>
    </tbody>
</table>

    <br>
    
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

const companies = ref([]);
const students = ref([]);
const jobs = ref([]);
const applications = ref([]);

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
    loadCompanies();
    loadStudents();
    loadJobs();
    loadApplications();
});
async function loadStats() {
    try {
        const response = await api.get("/admin/stats");
        stats.value = response.data;
    } catch (error) {
        console.log(error);
    }
}

async function loadCompanies() {
    try {
        const response = await api.get("/admin/companies");
        companies.value = response.data;
        console.log(companies.value);
    } catch (error) {
        console.log(error);
    }
}

async function approveCompany(id) {
    try {
        await api.put(`/admin/company/${id}/approve`);
        loadCompanies();
        loadStats();
    } catch (error) {
        console.log(error);
    }
}

async function deactivateCompany(id) {
    try {
        await api.put(`/admin/company/${id}/deactivate`);
        loadCompanies();
        loadStats();
    } catch (error) {
        console.log(error);
    }
}

async function activateCompany(id) {
    try {
        await api.put(`/admin/company/${id}/activate`);
        loadCompanies();
        loadStats();
    } catch (error) {
        console.log(error);
    }
}

async function deactivateStudent(id) {
    try {
        await api.put(`/admin/student/${id}/deactivate`);
        loadStudents();
        loadStats();
    } catch (error) {
        console.log(error);
    }
}

async function activateStudent(id) {
    try {
        await api.put(`/admin/student/${id}/activate`);
        loadStudents();
        loadStats();
    } catch (error) {
        console.log(error);
    }
}

async function loadStudents() {
    try {
        const response = await api.get("/admin/students");
        students.value = response.data;
    } catch (error) {
        console.log(error);
    }
}

async function loadJobs() {
    try {
        const response = await api.get("/admin/jobs");
        jobs.value = response.data;
    } catch (error) {
        console.log(error);
    }
}

async function deleteJob(id) {
    try {
        await api.delete(`/admin/job/${id}`);

        loadJobs();
        loadStats();

    } catch (error) {
        console.log(error);
    }
}

async function loadApplications() {
    try {
        const response = await api.get("/admin/applications");
        applications.value = response.data;
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

.approve-btn{
    background:#198754;
    color:white;
    border:none;
    padding:8px 16px;
    border-radius:6px;
    cursor:pointer;
    margin-right:8px;
}

.approve-btn:hover{
    background:#157347;
}

.deactivate-btn{
    background:#dc3545;
    color:white;
    border:none;
    padding:8px 16px;
    border-radius:6px;
    cursor:pointer;
}

.deactivate-btn:hover{
    background:#bb2d3b;
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

.status{
    display:inline-block;
    padding:6px 14px;
    border-radius:20px;
    font-size:14px;
    font-weight:600;
}

.approved{
    background:#d1fae5;
    color:#065f46;
}

.pending{
    background:#fee2e2;
    color:#991b1b;
}

.success-btn{
    background:#198754;
    color:white;
}

.success-btn:hover{
    background:#157347;
}

</style>