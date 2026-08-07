<template>
<div style="padding:40px">

    <button @click="$router.back()">
        ← Back
    </button>

    <h1>{{ job.title || "Loading..." }}</h1>

    <br>

    <div class="card">

        <p><b>Salary:</b> ₹ {{ job.salary }}</p>

        <p><b>Location:</b> {{ job.location }}</p>

        <p><b>Deadline:</b> {{ job.deadline }}</p>

        <p><b>Description:</b></p>

        <p>{{ job.description }}</p>

    </div>

    <br><br>

    <h2>Applicants</h2>

    <table class="company-table">

        <thead>

            <tr>

                <th>Name</th>

                <th>CGPA</th>

                <th>Status</th>

                <th>Action</th>

            </tr>

        </thead>

        <tbody>

            <tr v-if="applications.length === 0">

                <td colspan="4">
                    No applications yet.
                </td>

            </tr>

            <tr
                v-for="application in applications"
                :key="application.application_id"
            >

                <td>{{ application.student_name }}</td>

                <td>{{ application.cgpa }}</td>

                <td>{{ application.status }}</td>

                <td>

                    <a
                        :href="application.resume_url"
                        target="_blank"
                        v-if="application.resume_url"
                    >
                        Resume
                    </a>

                    <span v-else>
                        No Resume
                    </span>

                </td>

            </tr>

        </tbody>

    </table>

</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "../services/app";

const route = useRoute();

const job = ref({});
const applications = ref([]);

async function loadJob() {

    try {

        const response = await api.get(
            `/company/job/${route.params.id}`
        );

        job.value = response.data;

    } catch (error) {
        console.log(error);
    }

}

async function loadApplications() {

    try {

        const response = await api.get(
            `/company/job/${route.params.id}/applications`
        );

        applications.value = response.data;

    } catch (error) {
        console.log(error);
    }

}

onMounted(() => {
    loadJob();
    loadApplications();
});
</script>

<style scoped>

.card{

    background:white;

    padding:25px;

    border-radius:12px;

    box-shadow:0 2px 10px rgba(0,0,0,.15);

}

.company-table{

    width:100%;

    border-collapse:collapse;

}

.company-table th{

    background:grey;

    color:white;

    padding:12px;

}

.company-table td{

    padding:12px;

    border-bottom:1px solid #ddd;

}

</style>