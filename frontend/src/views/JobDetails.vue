<template>
  <div style="padding:40px">

    <button @click="$router.back()">← Back</button>

    <br><br>

    <div class="card">

            <h1>{{ job.title }}</h1>

            <p><b>Company:</b> {{ job.company }}</p>

            <p><b>Salary:</b> ₹ {{ job.salary }}</p>

            <p><b>Location:</b> {{ job.location }}</p>

            <p><b>Deadline:</b> {{ job.deadline }}</p>

            <p><b>Description:</b></p>

            <p>{{ job.description }}</p>

            <p><b>Skills Required:</b></p>

            <p>{{ job.skills_required }}</p>

        <br>

        <div style="margin-top:30px">

    <button
        v-if="!applied"
        class="success-btn"
        @click="applyJob"
    >
        Apply
    </button>

    <button
        v-else
        disabled
        class="approve-btn"
    >
        {{ applicationStatus }}
    </button>

</div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "../services/app";

const route = useRoute();
const job = ref({});
const applied = ref(false);
const applicationStatus = ref("");


async function checkApplicationStatus() {

    try {
        const response = await api.get(
            `/student/job/${route.params.id}/status`
        );
        applied.value = response.data.applied;
        applicationStatus.value = response.data.status || "";

    } catch (error) {
        console.log(error);
    }

}


async function applyJob() {

    try {
        await api.post(
            `/student/job/${route.params.id}/apply`
        );
        applied.value = true;
        applicationStatus.value = "Applied";
        alert("Applied Successfully!");
    } catch (error) {
        alert(error.response.data.error);
    }
}


async function loadJob() {

    try {

        const response = await api.get(`/student/job/${route.params.id}`);

        job.value = response.data;

    } catch (error) {

        console.log(error);

    }

}

onMounted(() => {

    loadJob();
    checkApplicationStatus();

});
</script>

<style scoped>

.card{

    background:white;

    padding:30px;

    border-radius:12px;

    box-shadow:0 2px 10px rgba(0,0,0,.15);

}

.apply-btn{

    background:#198754;

    color:white;

    border:none;

    padding:10px 20px;

    border-radius:6px;

    cursor:pointer;

}
.success-btn{
    background:#198754;
    color:white;
    border:none;
    padding:12px 30px;
    border-radius:8px;
    cursor:pointer;
    font-size:16px;
}

.success-btn:hover{
    background:#157347;
}

.approve-btn{
    background:#6c757d;
    color:white;
    border:none;
    padding:12px 30px;
    border-radius:8px;
    font-size:16px;
}

</style>