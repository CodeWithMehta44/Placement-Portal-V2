<template>
  <div>
    <h1>StudentDashboard Page</h1>
    <h2>Available Jobs</h2>

<table class="company-table">

    <thead>
        <tr>
            <th>Company</th>
            <th>Title</th>
            <th>Salary</th>
            <th>Location</th>
            <th>Deadline</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>

        <tr
            v-for="job in jobs"
            :key="job.id"
        >
            <td>{{ job.company }}</td>
            <td>{{ job.title }}</td>
            <td>₹ {{ job.salary }}</td>
            <td>{{ job.location }}</td>
            <td>{{ job.deadline }}</td>
            <td>
                <button
                class="approve-btn"
                @click="$router.push(`/student/job/${job.id}`)"
            >
                View Details
            </button>
            </td>
        </tr>

    </tbody>

</table>
<h2 style="margin-top:50px;">
    My Applications
</h2>
<table class="company-table">

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

            <td>{{ application.status }}</td>

            <td>{{ application.applied_date }}</td>

            <td>

                <button class="approve-btn">

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


async function loadJobs() {

    try {

        const response = await api.get("/student/jobs");

        jobs.value = response.data;

    } catch (error) {

        console.log(error);

    }

}

onMounted(() => {

    loadJobs();
    loadApplications();

});
</script>

<style scoped>
div{
  padding:40px;
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
    background:#198754;
    color:white;
    border:none;
    padding:8px 16px;
    border-radius:6px;
    cursor:pointer;
}

.approve-btn:hover{
    background:#157347;
}
</style>