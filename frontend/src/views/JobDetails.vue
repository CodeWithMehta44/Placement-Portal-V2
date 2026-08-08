<template>
  <div style="padding:40px">

    <button @click="$router.back()" class="back-btn">
      ← Back
    </button>

    <div class="card">

      <div class="job-header">

        <div>

          <h1>{{ job.title }}</h1>

          <p class="company-name">
            {{ job.company }}
          </p>

        </div>

        <div class="salary-box">

          ₹ {{ job.salary }}

        </div>

      </div>

      <div class="job-meta">

        <span> {{ job.location }}</span>

        <span> {{ job.deadline }}</span>

      </div>

      <hr>

      <h3>Description</h3>

      <p>
        {{ job.description }}
      </p>

      <h3>Skills Required</h3>

      <p>
        {{ job.skills_required }}
      </p>

      <div class="apply-section">

        <button
          v-if="!applied"
          class="success-btn"
          @click="applyJob"
        >
          Apply Now
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
    padding:40px;
    border-radius:16px;
    box-shadow:0 8px 25px rgba(0,0,0,.08);
    max-width:900px;
    /* margin:auto; */
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
.back-btn{
    background:#fff;
    border:1px solid #ddd;
    padding:10px 18px;
    border-radius:8px;
    cursor:pointer;
    font-weight:600;
    transition:.3s;
}

.back-btn:hover{
    background:#198754;
    color:white;
}

.job-header{
    display:flex;
    justify-content:space-between;
    align-items:flex-start;
    margin-bottom:25px;
}

.job-header h1{
    margin:0;
    font-size:34px;
}

.company-name{
    color:#666;
    font-size:18px;
    margin-top:8px;
}

.salary-box{
    font-size:28px;
    font-weight:bold;
    padding:12px 24px;
    border-radius:30px;
}

.job-meta{
    display:flex;
    gap:40px;
    margin:25px 0;
    color:#555;
    font-size:17px;
}

.card h3{
    margin-top:25px;
    margin-bottom:10px;
}

.card p{
    line-height:1.7;
}

.apply-section{
    margin-top:35px;
    display:flex;
    justify-content:flex-end;
}
</style>