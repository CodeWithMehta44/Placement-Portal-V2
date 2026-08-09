<template>
  <div class="register-page">

    <div class="register-card">

      <!-- Header -->
      <div class="header">
        <h1>Placement Portal</h1>
        <p>Create your account</p>
      </div>


      <!-- Role Selection -->
      <div class="role-section" v-if="!registrationSuccess">

        <p class="role-title">Register as</p>

        <div class="role-buttons">

          <button
            type="button"
            :class="{ active: role === 'student' }"
            @click="selectRole('student')"
          >
            <span class="role-icon">🎓</span>
            Student
          </button>

          <button
            type="button"
            :class="{ active: role === 'company' }"
            @click="selectRole('company')"
          >
            <span class="role-icon">🏢</span>
            Company
          </button>

        </div>

      </div>


      <!-- Error Message -->
      <div
        v-if="errorMessage"
        class="error-message"
      >
        {{ errorMessage }}
      </div>


      <!-- ========================= -->
      <!-- COMPANY SUCCESS MESSAGE -->
      <!-- ========================= -->

      <div
        v-if="registrationSuccess && role === 'company'"
        class="success-container"
      >

        <div class="success-icon">
          ✓
        </div>

        <h2>Registration Successful!</h2>

        <p>
          Your company has been registered successfully.
        </p>

        <p class="approval-message">
          Your account is currently waiting for
          <strong>admin approval</strong>.
        </p>

        <p class="small-message">
          You will be able to access the company portal
          after the administrator approves your account.
        </p>

        <button
          type="button"
          class="login-button"
          @click="goToLogin"
        >
          Go to Login
        </button>

      </div>


      <!-- ========================= -->
      <!-- STUDENT SUCCESS MESSAGE -->
      <!-- ========================= -->

      <div
        v-if="registrationSuccess && role === 'student'"
        class="success-container"
      >

        <div class="success-icon">
          ✓
        </div>

        <h2>Registration Successful!</h2>

        <p>
          Your student account has been created successfully.
        </p>

        <p class="small-message">
          Redirecting you to the login page...
        </p>

      </div>


      <!-- ========================= -->
      <!-- STUDENT FORM -->
      <!-- ========================= -->

      <form
        v-if="!registrationSuccess && role === 'student'"
        @submit.prevent="registerStudent"
      >

        <!-- Name -->
        <div class="form-group">

          <label>Full Name</label>

          <input
            type="text"
            v-model="studentForm.name"
            placeholder="Enter your full name"
            autocomplete="name"
            required
          />

        </div>


        <!-- Email -->
        <div class="form-group">

          <label>Email</label>

          <input
            type="email"
            v-model="studentForm.email"
            placeholder="Enter your email"
            autocomplete="email"
            required
          />

        </div>


        <!-- Password -->
        <div class="form-group">

          <label>Password</label>

          <input
            type="password"
            v-model="studentForm.password"
            placeholder="Create a password"
            autocomplete="new-password"
            required
          />

        </div>


        <!-- Confirm Password -->
        <div class="form-group">

          <label>Confirm Password</label>

          <input
            type="password"
            v-model="studentForm.confirmPassword"
            placeholder="Confirm your password"
            autocomplete="new-password"
            required
          />

        </div>


        <!-- Register -->
        <button
          class="register-button"
          type="submit"
          :disabled="loading"
        >
          {{ loading ? "Creating Account..." : "Create Student Account" }}
        </button>

      </form>


      <!-- ========================= -->
      <!-- COMPANY FORM -->
      <!-- ========================= -->

      <form
        v-if="!registrationSuccess && role === 'company'"
        @submit.prevent="registerCompany"
      >

        <!-- Company Name -->
        <div class="form-group">

          <label>Company Name</label>

          <input
            type="text"
            v-model="companyForm.company_name"
            placeholder="Enter company name"
            required
          />

        </div>


        <!-- Industry -->
        <div class="form-group">

          <label>Industry</label>

          <input
            type="text"
            v-model="companyForm.industry"
            placeholder="e.g. Technology, Finance, Healthcare"
            required
          />

        </div>


        <!-- Location -->
        <div class="form-group">

          <label>Location</label>

          <input
            type="text"
            v-model="companyForm.location"
            placeholder="e.g. Bangalore"
            required
          />

        </div>


        <!-- Email -->
        <div class="form-group">

          <label>Company Email</label>

          <input
            type="email"
            v-model="companyForm.email"
            placeholder="Enter company email"
            autocomplete="email"
            required
          />

        </div>


        <!-- Password -->
        <div class="form-group">

          <label>Password</label>

          <input
            type="password"
            v-model="companyForm.password"
            placeholder="Create a password"
            autocomplete="new-password"
            required
          />

        </div>


        <!-- Website -->
        <div class="form-group">

          <label>
            Website
            <span>(Optional)</span>
          </label>

          <input
            type="url"
            v-model="companyForm.website"
            placeholder="https://example.com"
          />

        </div>


        <!-- Description -->
        <div class="form-group">

          <label>
            Description
            <span>(Optional)</span>
          </label>

          <textarea
            v-model="companyForm.description"
            placeholder="Tell us about your company"
            rows="3"
          ></textarea>

        </div>


        <!-- Register -->
        <button
          class="register-button"
          type="submit"
          :disabled="loading"
        >
          {{ loading ? "Registering Company..." : "Register Company" }}
        </button>

      </form>


      <!-- Login Link -->
      <div
        class="login-link"
        v-if="!registrationSuccess"
      >

        Already have an account?

        <router-link to="/">
          Login
        </router-link>

      </div>

    </div>

  </div>
</template>


<script setup>

import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/app.js";


// Router
const router = useRouter();


// Selected role
const role = ref("student");


// Loading state
const loading = ref(false);


// Messages
const errorMessage = ref("");


// Registration success
const registrationSuccess = ref(false);


// =========================
// STUDENT FORM
// =========================

const studentForm = ref({

  name: "",

  email: "",

  password: "",

  confirmPassword: ""

});


// =========================
// COMPANY FORM
// =========================

const companyForm = ref({

  company_name: "",

  industry: "",

  location: "",

  email: "",

  password: "",

  website: "",

  description: ""

});


// =========================
// SELECT ROLE
// =========================

function selectRole(selectedRole) {

  role.value = selectedRole;

  errorMessage.value = "";

  registrationSuccess.value = false;

}


// =========================
// GO TO LOGIN
// =========================

function goToLogin() {

  router.push("/");

}


// =========================
// STUDENT REGISTRATION
// =========================

async function registerStudent() {

  errorMessage.value = "";

  registrationSuccess.value = false;


  // Check password
  if (
    studentForm.value.password !==
    studentForm.value.confirmPassword
  ) {

    errorMessage.value =
      "Passwords do not match.";

    return;

  }


  // Minimum password length
  if (studentForm.value.password.length < 6) {

    errorMessage.value =
      "Password must be at least 6 characters.";

    return;

  }


  loading.value = true;


  try {

    const response = await api.post(
      "/register",
      {

        name: studentForm.value.name,

        email: studentForm.value.email,

        password: studentForm.value.password

      }
    );


    console.log(
      "Student registration:",
      response.data
    );


    registrationSuccess.value = true;


    // Redirect student to login
    setTimeout(() => {

      router.push("/");

    }, 1500);


  } catch (error) {

    console.error(error);


    errorMessage.value =
      error.response?.data?.error ||
      "Registration failed. Please try again.";

  } finally {

    loading.value = false;

  }

}


// =========================
// COMPANY REGISTRATION
// =========================

async function registerCompany() {

  errorMessage.value = "";

  registrationSuccess.value = false;


  // Minimum password length
  if (companyForm.value.password.length < 6) {

    errorMessage.value =
      "Password must be at least 6 characters.";

    return;

  }


  loading.value = true;


  try {

    const response = await api.post(
      "/company/register",
      {

        company_name:
          companyForm.value.company_name,

        industry:
          companyForm.value.industry,

        location:
          companyForm.value.location,

        email:
          companyForm.value.email,

        password:
          companyForm.value.password,

        website:
          companyForm.value.website,

        description:
          companyForm.value.description

      }
    );


    console.log(
      "Company registration:",
      response.data
    );


    registrationSuccess.value = true;


    // Clear company form
    companyForm.value = {

      company_name: "",

      industry: "",

      location: "",

      email: "",

      password: "",

      website: "",

      description: ""

    };


    // IMPORTANT:
    // Company does NOT automatically redirect.
    // They need to read the approval message
    // and click "Go to Login".

  } catch (error) {

    console.error(error);


    errorMessage.value =
      error.response?.data?.error ||
      "Company registration failed. Please try again.";

  } finally {

    loading.value = false;

  }

}

</script>


<style scoped>

* {
  box-sizing: border-box;
}


/* ========================= */
/* PAGE */
/* ========================= */

.register-page {

  min-height: 100vh;

  display: flex;

  justify-content: center;

  align-items: center;

  padding: 30px;

  background:
    linear-gradient(
      135deg,
      #eef4ff,
      #f8faff
    );

}


/* ========================= */
/* CARD */
/* ========================= */

.register-card {

  width: 100%;

  max-width: 480px;

  background: white;

  padding: 35px;

  border-radius: 18px;

  box-shadow:
    0 15px 40px
    rgba(0, 0, 0, 0.12);

}


/* ========================= */
/* HEADER */
/* ========================= */

.header {

  text-align: center;

  margin-bottom: 28px;

}


.header h1 {

  margin: 0;

  font-size: 30px;

  color: #111827;

}


.header p {

  margin-top: 8px;

  margin-bottom: 0;

  color: #6b7280;

  font-size: 15px;

}


/* ========================= */
/* ROLE SECTION */
/* ========================= */

.role-section {

  margin-bottom: 25px;

}


.role-title {

  margin-bottom: 10px;

  font-weight: 600;

  color: #374151;

}


.role-buttons {

  display: flex;

  gap: 12px;

}


.role-buttons button {

  flex: 1;

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 8px;

  padding: 13px;

  border: 2px solid #e5e7eb;

  background: white;

  color: #374151;

  border-radius: 10px;

  cursor: pointer;

  font-size: 15px;

  font-weight: 600;

  transition: 0.2s;

}


.role-buttons button:hover {

  border-color: #2563eb;

}


.role-buttons button.active {

  background: #2563eb;

  border-color: #2563eb;

  color: white;

}


.role-icon {

  font-size: 18px;

}


/* ========================= */
/* FORM */
/* ========================= */

.form-group {

  margin-bottom: 17px;

}


.form-group label {

  display: block;

  margin-bottom: 7px;

  font-size: 14px;

  font-weight: 600;

  color: #374151;

}


.form-group label span {

  color: #9ca3af;

  font-weight: normal;

}


input,
textarea {

  width: 100%;

  padding: 12px 13px;

  border: 1px solid #d1d5db;

  border-radius: 9px;

  font-size: 14px;

  outline: none;

  transition: 0.2s;

  font-family: inherit;

}


input:focus,
textarea:focus {

  border-color: #2563eb;

  box-shadow:
    0 0 0 3px
    rgba(37, 99, 235, 0.1);

}


textarea {

  resize: vertical;

}


/* ========================= */
/* REGISTER BUTTON */
/* ========================= */

.register-button {

  width: 100%;

  padding: 13px;

  margin-top: 5px;

  border: none;

  border-radius: 9px;

  background: #2563eb;

  color: white;

  font-size: 15px;

  font-weight: 600;

  cursor: pointer;

  transition: 0.2s;

}


.register-button:hover {

  background: #1d4ed8;

}


.register-button:disabled {

  background: #93c5fd;

  cursor: not-allowed;

}


/* ========================= */
/* ERROR */
/* ========================= */

.error-message {

  background: #fef2f2;

  color: #dc2626;

  border: 1px solid #fecaca;

  padding: 12px;

  border-radius: 9px;

  margin-bottom: 18px;

  font-size: 14px;

}


/* ========================= */
/* SUCCESS */
/* ========================= */

.success-container {

  text-align: center;

  padding: 10px 5px 5px;

}


.success-icon {

  width: 58px;

  height: 58px;

  margin: 0 auto 15px;

  display: flex;

  align-items: center;

  justify-content: center;

  border-radius: 50%;

  background: #22c55e;

  color: white;

  font-size: 30px;

  font-weight: bold;

}


.success-container h2 {

  margin: 0 0 12px;

  color: #166534;

  font-size: 22px;

}


.success-container p {

  color: #374151;

  font-size: 14px;

  line-height: 1.6;

}


.approval-message {

  background: #fff7ed;

  border: 1px solid #fed7aa;

  color: #9a3412 !important;

  padding: 12px;

  border-radius: 9px;

  margin: 15px 0;

}


.small-message {

  color: #6b7280 !important;

  font-size: 13px !important;

}


/* ========================= */
/* LOGIN BUTTON */
/* ========================= */

.login-button {

  width: 100%;

  margin-top: 15px;

  padding: 13px;

  border: none;

  border-radius: 9px;

  background: #2563eb;

  color: white;

  font-size: 15px;

  font-weight: 600;

  cursor: pointer;

  transition: 0.2s;

}


.login-button:hover {

  background: #1d4ed8;

}


/* ========================= */
/* LOGIN LINK */
/* ========================= */

.login-link {

  text-align: center;

  margin-top: 23px;

  font-size: 14px;

  color: #6b7280;

}


.login-link a {

  color: #2563eb;

  font-weight: 600;

  text-decoration: none;

}


.login-link a:hover {

  text-decoration: underline;

}


/* ========================= */
/* MOBILE */
/* ========================= */

@media (max-width: 500px) {

  .register-page {

    padding: 15px;

  }


  .register-card {

    padding: 25px 20px;

  }


  .header h1 {

    font-size: 26px;

  }


  .role-buttons {

    flex-direction: column;

  }

}

</style>