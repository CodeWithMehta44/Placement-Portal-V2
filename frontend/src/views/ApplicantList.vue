<template>
<div class="page-container">

    <button class="back-btn" @click="$router.back()">
        ← Back
    </button>

   <h1 class="page-title">Applicants</h1>

    <p class="page-subtitle">
        Students who applied for this placement drive.
    </p>    
    <table class="company-table">

        <thead>
            <tr>
                <th>Student</th>
                <th>CGPA</th>
                <th>Resume</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>

            <tr v-if="applications.length === 0">
                <td colspan="5" class="empty-state">
                    No applicants yet.
                </td>
            </tr>

            <tr
                v-else
                v-for="student in applications"
                :key="student.application_id"
            >

                <td>{{ student.student_name }}</td>

                <td>{{ student.cgpa }}</td>

                <td>
                  <button
                        v-if="student.resume"
                        class="resume-link"
                        @click="viewResume(student.application_id)"
                    >
                        View Resume
                    </button>

                    <span v-else>
                        No Resume
                    </span>
                </td>

                <td>

                    <span
                        class="status-badge"
                        :class="student.status.toLowerCase()"
                    >
                        {{ student.status }}
                    </span>

                </td>
                <td>
           <td>

                <button
                    v-if="student.status === 'Applied'"
                    class="success-btn"
                    @click="updateStatus(student, 'Shortlisted')"
                >
                    Shortlist
                </button>

                <button
                    v-if="student.status === 'Applied'"
                    class="danger-btn"
                    @click="updateStatus(student, 'Rejected')"
                >
                    Reject
                </button>

                <button
                    v-else-if="student.status === 'Shortlisted'"
                    class="success-btn"
                    @click="scheduleInterview(student)"
                >
                    Schedule Interview
                </button>

                <template v-else-if="student.status === 'Interview'">
                    <button
                        class="success-btn"
                        @click="updateStatus(student, 'Selected')"
                    >
                        Select
                    </button>

                    <button
                        class="danger-btn"
                        @click="updateStatus(student, 'Rejected')"
                    >
                        Reject
                    </button>
                </template>

                <span v-else class="action-done">
                    Action Completed
                </span>

            </td>
                </td>

            </tr>

        </tbody>

    </table>

    <div
    v-if="showInterviewModal"
    class="modal-overlay"
>

<div class="modal">

<h2>Schedule Interview</h2>

<label>Date</label>

<input
type="date"
v-model="interviewForm.interview_date"
/>

<label>Time</label>

<input
type="time"
v-model="interviewForm.interview_time"
/>

<label>Location</label>

<input
type="text"
placeholder="Interview Location"
v-model="interviewForm.interview_location"
/>

<div class="modal-buttons">

<button
class="danger-btn"
@click="showInterviewModal=false"
>
Cancel
</button>

<button
class="success-btn"
@click="confirmInterview"
>
Schedule
</button>

</div>

</div>

</div>

</div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import api from "../services/app";

const route = useRoute();

const applications = ref([]);

const showInterviewModal = ref(false)

const selectedStudent = ref(null)

const interviewForm = ref({
    interview_date: "",
    interview_time: "",
    interview_location: ""
})

function scheduleInterview(student){

    selectedStudent.value = student

    interviewForm.value = {
        interview_date:"",
        interview_time:"",
        interview_location:""
    }

    showInterviewModal.value = true

}

async function confirmInterview(){

    try{

        await api.put(
            `/company/application/${selectedStudent.value.application_id}/interview`,
            interviewForm.value
        )

        selectedStudent.value.status = "Interview"

        showInterviewModal.value = false

        alert("Interview Scheduled Successfully!")

    }

    catch(error){

        alert(error.response?.data?.error || "Something went wrong")

    }

}

async function loadApplicants() {

    try {

        const response = await api.get(
            `/company/job/${route.params.id}/applications`
        );

          applications.value = response.data;

    console.log(applications.value);

    }

    catch(error) {
        console.log(error);
    }

}

async function updateStatus(app, status) {

    try {

        await api.put(
            `/company/application/${app.application_id}`,
            {
                status: status
            }
        )

        app.status = status

        alert("Status Updated!")

    }

    catch (error) {

        alert(error.response?.data?.error || "Something went wrong")

    }

}

async function viewResume(applicationId) {
    try {
        const response = await api.get(
            `/company/application/${applicationId}/resume`,
            {
                responseType: "blob"
            }
        )

        const fileURL = URL.createObjectURL(response.data)

        window.open(fileURL, "_blank")

    } catch (error) {
        alert(
            error.response?.data?.error ||
            "Unable to open resume"
        )
    }
}

onMounted(() => {

    loadApplicants();

});
</script>

<style scoped>

.page-container{
    max-width:1200px;
    margin:auto;
    padding:40px;
}

.page-title{
    font-size:44px;
    font-weight:700;
    margin-top:20px;
}

.page-subtitle{
    color:#666;
    margin-bottom:35px;
}

.company-table{
    width:100%;
    border-collapse:separate;
    border-spacing:0;
    background:#fff;
    border-radius:15px;
    overflow:hidden;
    box-shadow:0 8px 25px rgba(0,0,0,.08);
}

.company-table th{
    background:#198754;
    color:white;
    padding:18px;
    font-size:17px;
    text-align:left;
}

.company-table td{
    padding:20px 18px;
    border-bottom:1px solid #f1f1f1;
    font-size:16px;
}

.company-table tbody tr:hover{
    background:#f5f7f9;
}

.status-badge{
    display:inline-block;
    padding:8px 18px;
    border-radius:20px;
    font-weight:600;
    background:#d1fae5;
    color:#198754;
}

.status-badge.applied{
    background:#d1fae5;
    color:#198754;
}

.status-badge.shortlisted{
    background:#dbeafe;
    color:#2563eb;
}

.status-badge.interview{
    background:#ede9fe;
    color:#7c3aed;
}

.status-badge.selected{
    background:#dcfce7;
    color:#15803d;
}

.status-badge.rejected{
    background:#fee2e2;
    color:#dc2626;
}

.back-btn{
    border:none;
    background:none;
    font-size:18px;
    cursor:pointer;
    margin-bottom:20px;
    color:#444;
    transition:.2s;
}
.empty-state{
    text-align:center;
    padding:40px;
    color:#777;
    font-size:18px;
}

.back-btn:hover{
    color:#198754;
}

.success-btn{
    background:#198754;
    color:white;
    border:none;
    padding:8px 16px;
    border-radius:6px;
    cursor:pointer;
    margin-right:8px;
}

.success-btn:hover{
    background:#157347;
}

.danger-btn{
    background:#dc3545;
    color:white;
    border:none;
    padding:10px 18px;
    border-radius:8px;
    cursor:pointer;
    font-weight:600;
    transition:.25s;
}

.success-btn:hover,
.danger-btn:hover{
    transform:translateY(-2px);
}
.action-done{
    color:#777;
    font-weight:600;
}

.resume-link{
    color:#198754;
    font-weight:600;
    text-decoration:none;
}

.resume-link:hover{
    text-decoration:underline;
}

.modal-overlay{

    position:fixed;

    inset:0;

    background:rgba(0,0,0,.45);

    display:flex;

    justify-content:center;

    align-items:center;

    z-index:999;

}

.modal{

    width:420px;

    background:white;

    border-radius:15px;

    padding:30px;

    box-shadow:0 15px 40px rgba(0,0,0,.2);

}

.modal h2{

    margin-bottom:25px;

}

.modal label{

    display:block;

    margin-top:15px;

    margin-bottom:6px;

    font-weight:600;

}

.modal input{

    width:100%;

    padding:10px;

    border:1px solid #ccc;

    border-radius:8px;

}

.modal-buttons{

    display:flex;

    justify-content:flex-end;

    gap:10px;

    margin-top:25px;

}

</style>