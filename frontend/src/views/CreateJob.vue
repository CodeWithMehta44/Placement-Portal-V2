<template>
  <div class="container">

    <button class="back-btn" @click="$router.back()">
      ← Back
    </button>

    <div class="form-card">

      <h1>Create Placement Drive</h1>
      <p>Fill in the details below.</p>

      <form>

        <div class="form-group">
          <label>Job Title</label>
          <input type="text" v-model="title" placeholder="Software Engineer">
        </div>

        <div class="form-group">
          <label>Salary (LPA)</label>
          <input type="number" v-model="salary" placeholder="12">
        </div>

        <div class="form-group">
          <label>Location</label>
          <input type="text" v-model="location" placeholder="Bangalore">
        </div>

        <div class="form-group">
          <label>Application Deadline</label>
          <input type="date" v-model="deadline">
        </div>

        <div class="form-group">
          <label>Description</label>
          <textarea rows="4" v-model="description"></textarea>
        </div>

        <div class="form-group">
          <label>Skills Required</label>
          <textarea rows="3" v-model="skills_required" placeholder="Python, Flask, SQL"></textarea>
        </div>

        <div>
          <label>Vacancies</label>
                <input
                type="number"
                v-model="vacancies"
                placeholder="10"
                />
          </div>

        <button class="create-btn" @click="submitForm">
          Create Placement Drive
        </button>

      </form>

    </div>

  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router"
import api from "../services/app"

const router = useRouter()

const title = ref("")
const salary = ref("")
const location = ref("")
const deadline = ref("")
const description = ref("")
const skills_required = ref("")
const vacancies = ref("")

// async function createJob() {
//   try {

//     await api.post("/company/job", {
//       title: title.value,
//       description: description.value,
//       salary: salary.value,
//       location: location.value,
//       skills_required: skills_required.value,
//       vacancies: vacancies.value,
//       deadline: deadline.value
//     })

//     alert("Job Created Successfully!")

//     router.push("/company")

//   } catch (error) {

//     alert(error.response.data.error)

//   }
// }
async function submitForm() {

  console.log("Submit Clicked");
    try {
        await api.post("/company/job", {
            title: title.value,
            description: description.value,
            salary: salary.value,
            location: location.value,
            skills_required: skills_required.value,
            vacancies: vacancies.value,
            deadline: deadline.value
        });

        alert("Job Created Successfully!");

        router.push("/company");

    } catch (error) {
        alert(error.response?.data?.error || "Something went wrong");
    }
    
}
</script>
<style scoped>

.container{
    padding:40px;
}

.back-btn{
    background:none;
    border:none;
    font-size:18px;
    cursor:pointer;
    margin-bottom:25px;
}

.form-card{
    max-width:700px;
    margin:auto;
    background:white;
    padding:35px;
    border-radius:15px;
    box-shadow:0 4px 15px rgba(0,0,0,.1);
}

.form-card h1{
    margin-bottom:10px;
}

.form-card p{
    color:#666;
    margin-bottom:30px;
}

.form-group{
    margin-bottom:20px;
}

label{
    display:block;
    margin-bottom:8px;
    font-weight:bold;
}

input,
textarea{
    width:100%;
    padding:12px;
    border:1px solid #ccc;
    border-radius:8px;
    font-size:15px;
    box-sizing:border-box;
}

input:focus,
textarea:focus{
    outline:none;
    border-color:#198754;
}

.create-btn{
    width:100%;
    padding:14px;
    background:#198754;
    color:white;
    border:none;
    border-radius:8px;
    font-size:16px;
    cursor:pointer;
    transition:.3s;
}

.create-btn:hover{
    background:#157347;
}

</style>