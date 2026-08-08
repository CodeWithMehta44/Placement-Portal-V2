<template>
  <div class="profile-container">

    <div class="profile-header">
      <h1>Student Profile</h1>

      <button
        class="edit-btn"
        @click="editing = !editing"
      >
        {{ editing ? "Cancel" : "Edit Profile" }}
      </button>
    </div>

    <div class="profile-card">

      <div class="form-group">
        <label>Full Name</label>
        <input v-model="student.full_name" :disabled="!editing">
      </div>

      <div class="form-group">
        <label>Email</label>
        <input v-model="student.email" disabled>
      </div>

      <div class="form-group">
        <label>College</label>
        <input v-model="student.college" :disabled="!editing">
      </div>

      <div class="form-group">
        <label>Degree</label>
        <input v-model="student.degree" :disabled="!editing">
      </div>

      <div class="form-group">
        <label>Branch</label>
        <input v-model="student.branch" :disabled="!editing">
      </div>

      <div class="form-group">
        <label>CGPA</label>
        <input v-model="student.cgpa" :disabled="!editing">
      </div>

      <div class="form-group">
        <label>Graduation Year</label>
        <input v-model="student.graduation_year" :disabled="!editing">
      </div>

      <div class="form-group">
        <label>Phone</label>
        <input v-model="student.phone" :disabled="!editing">
      </div>

      <div class="form-group">
        <label>Skills</label>
        <textarea
          v-model="student.skills"
          :disabled="!editing"
        ></textarea>
      </div>

      <div class="form-group">
        <label>GitHub</label>
        <input v-model="student.github" :disabled="!editing">
      </div>

      <div class="form-group">
        <label>LinkedIn</label>
        <input v-model="student.linkedin" :disabled="!editing">
      </div>

    <div class="form-group">
    <label>Resume</label>

    <p v-if="student.resume">
        📄 {{ student.resume }}
    </p>

    <div v-if="editing">
       <input
        type="file"
        accept=".pdf"
        @change="resumeFile = $event.target.files[0]"
    >

        <button
            class="save-btn"
            type="button"
            @click="uploadResume"
        >
            Upload Resume
        </button>
    </div>
  </div>

      <button
        v-if="editing"
        class="save-btn"
        @click="saveProfile"
      >
        Save Changes
      </button>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/app";

const student = ref({});
const editing = ref(false);
const resumeFile = ref(null);


async function uploadResume() {
    if (!resumeFile.value) {
        alert("Please select a PDF file first.");
        return;
    }

    const formData = new FormData();
    formData.append("resume", resumeFile.value);

    try {
        const response = await api.post(
            "/student/profile/resume",
            formData
        );

        alert(response.data.message);

        resumeFile.value = null;

        await loadProfile();

    } catch (error) {
        console.error(error);

        if (error.response) {
            alert(error.response.data.message || "Resume upload failed");
        } else {
            alert("Resume upload failed");
        }
    }
}

async function loadProfile() {
    try {
        const response = await api.get("/student/profile");
        student.value = response.data;
    }
    catch (error) {
        console.log(error);
    }
}

async function saveProfile() {

    try {
        await api.put("/student/profile", student.value);

        alert("Profile Updated Successfully");

        editing.value = false;

        loadProfile();

    } catch (error) {
        console.log(error);
    }

}

onMounted(() => {
    loadProfile();
});
</script>

<style scoped>

.profile-container{
    max-width:900px;
    margin:auto;
    padding:40px;
}

.profile-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:30px;
}

.profile-card{
    background:white;
    padding:30px;
    border-radius:12px;
    box-shadow:0 2px 10px rgba(0,0,0,.15);
}

.form-group{
    display:flex;
    flex-direction:column;
    margin-bottom:18px;
}

label{
    font-weight:bold;
    margin-bottom:6px;
}

input,
textarea{
    padding:10px;
    border:1px solid #ddd;
    border-radius:8px;
}

.edit-btn,
.save-btn{
    padding:10px 20px;
    border:none;
    border-radius:8px;
    color:white;
    cursor:pointer;
}

.edit-btn{
    background:#1976d2;
}

.save-btn{
    background:#198754;
}

</style>