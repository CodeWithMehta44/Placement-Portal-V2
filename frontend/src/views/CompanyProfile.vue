<template>
  <div class="profile-container">
    <h1>Company Profile</h1>

    <div class="profile-card">
        <div v-if="!editing">
            <h2>{{ company.name }}</h2>
        </div>

            <input
            v-else
            v-model="company.name"
            class="input"
            />

            <div>
                

                <span v-if="!editing">
                    <strong>Email:</strong>
                    {{ company.email }}
                </span>

                <input
                    v-else
                    v-model="company.email"
                    class="input"
                />
            </div>

            <div>
                

                <span v-if="!editing">
                    <strong>Website:</strong>
                    {{ company.website }}
                </span>

                <input
                    v-else
                    v-model="company.website"
                    class="input"
                />
            </div>
            <div>
                

                <span v-if="!editing">
                    <strong>Industry:</strong>
                    {{ company.industry }}
                </span>

                <input
                    v-else
                    v-model="company.industry"
                    class="input"
                />
            </div>
               
                <div v-if="!editing">
                     <p><strong>Description:</strong></p>
                     {{ company.description }}
                </div>
                <textarea
                    v-else
                    v-model="company.description"
                    class="textarea"
                ></textarea>

            <div>
                

                <span v-if="!editing">
                    <strong>Location:</strong>
                    {{ company.location }}
                </span>

                <input
                    v-else
                    v-model="company.location"
                    class="input"
            />
        </div>

        <div class="button-group">

            <button
                v-if="editing"
                class="save-btn"
                @click="saveProfile"
            >
                Save Changes
            </button>

            <button
                class="edit-btn"
                @click="editing = !editing"
            >
                {{ editing ? "Cancel" : "Edit Profile" }}
            </button>

</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/app";

const company = ref({
  name: "",
  email: "",
  website: "",
  industry: "",
  location: "",
  description: ""
});

const editing = ref(false)

async function loadProfile() {
  try {
    const response = await api.get("/company/profile");

    company.value = {
      name: response.data.company_name,
      email: response.data.email,
      website: response.data.website,
      industry: response.data.industry,
      location: response.data.location,
      description: response.data.description
    };
  } catch (err) {
    console.error(err);
  }
}

async function saveProfile() {
    try {
        await api.put("/company/profile", {
            company_name: company.value.name,
            email: company.value.email,
            website: company.value.website,
            industry: company.value.industry,
            location: company.value.location,
            description: company.value.description
        });

        editing.value = false;

        alert("Profile updated successfully!");

    } catch (err) {
        console.error(err);
        alert("Failed to update profile.");
    }
}
onMounted(() => {
  loadProfile();
});
</script>

<style scoped>
.profile-container{
    padding:40px;
}

.profile-card{
    background:white;
    padding:30px;
    border-radius:12px;
    box-shadow:0 4px 15px rgba(0,0,0,.08);
    max-width:700px;
}

.profile-card p{
    margin:12px 0;
}

.edit-btn{
    margin-top:20px;
    background:#198754;
    color:white;
    border:none;
    padding:12px 20px;
    border-radius:8px;
    cursor:pointer;
}
.input,
.textarea{
    width:100%;
    margin-top:8px;
    margin-bottom:18px;
    padding:10px;
    border:1px solid #ccc;
    border-radius:8px;
    font-size:16px;
}

.textarea{
    min-height:120px;
    resize:vertical;
}
.button-group{
    display:flex;
    gap:15px;
    margin-top:25px;
}

.save-btn{
    margin-top:20px;
    background:#198754;
    color:white;
    border:none;
    padding:12px 20px;
    border-radius:8px;
    cursor:pointer;
}

.save-btn:hover{
    background:#15803d;
}
</style>