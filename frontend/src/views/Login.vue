<template>
  <div class="login-page">
    <div class="login-card">

      <!-- Header -->
      <div class="brand-section">
        <!-- <div class="logo"></div> -->
        <h1>Placement Portal</h1>
        <p>Welcome back! Sign in to continue.</p>
      </div>

      <!-- Login Form -->
      <form @submit.prevent="login">

        <!-- Error Message -->
        <div v-if="errorMessage" class="error-message">
           {{ errorMessage }}
        </div>

        <!-- Email -->
        <div class="form-group">
          <label for="email">Email Address</label>

          <div class="input-wrapper">
            <span class="input-icon"></span>

            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="Enter your email"
              autocomplete="email"
              required
            />
          </div>
        </div>

        <!-- Password -->
        <div class="form-group">
          <label for="password">Password</label>

          <div class="input-wrapper">
            <span class="input-icon"></span>

            <input
              id="password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Enter your password"
              autocomplete="current-password"
              required
            />

            <button
              type="button"
              class="password-toggle"
              @click="showPassword = !showPassword"
            >
              {{ showPassword ? "Hide" : "Show" }}
            </button>
          </div>
        </div>

        <!-- Login Button -->
        <button
          type="submit"
          class="login-button"
          :disabled="loading"
        >
          <span v-if="loading">Signing in...</span>
          <span v-else>Sign In</span>
        </button>

      </form>

      <!-- Register -->
      <div class="register-section">
        <span>Don't have an account?</span>

        <router-link to="/register">
          Create an account
        </router-link>
      </div>

      <!-- Footer -->
      <!-- <div class="footer">
        Placement Portal • Secure Login
      </div> -->

    </div>
  </div>
</template>


<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/app";

const router = useRouter();

const email = ref("");
const password = ref("");

const showPassword = ref(false);
const loading = ref(false);
const errorMessage = ref("");


async function login() {

  errorMessage.value = "";

  // Basic validation
  if (!email.value.trim()) {
    errorMessage.value = "Please enter your email address.";
    return;
  }

  if (!password.value) {
    errorMessage.value = "Please enter your password.";
    return;
  }

  loading.value = true;

  try {

    const response = await api.post("/login", {
      email: email.value.trim(),
      password: password.value
    });

    console.log("Login Success:", response.data);

    // Save JWT token
    localStorage.setItem(
      "token",
      response.data.access_token
    );

    // Save role
    localStorage.setItem(
      "role",
      response.data.user.role
    );

    const role = response.data.user.role;

    // Redirect based on role
    if (role === "admin") {

      router.push("/admin");

    } else if (role === "company") {

      router.push("/company");

    } else {

      router.push("/student");

    }

  } catch (error) {

    console.error("Login Error:", error);

    if (error.response) {

      if (error.response.status === 401) {
        errorMessage.value =
          "Invalid email or password.";
      } else {
        errorMessage.value =
          error.response.data?.error ||
          error.response.data?.message ||
          "Login failed. Please try again.";
      }

    } else {

      errorMessage.value =
        "Unable to connect to the server.";

    }

  } finally {

    loading.value = false;

  }
}
</script>


<style scoped>

* {
  box-sizing: border-box;
}




.login-page {
  min-height: 100vh;

  display: flex;
  justify-content: center;
  align-items: center;

  padding: 30px;

  background:
    linear-gradient(
      135deg,
      #eef4ff 0%,
      #f8fbff 50%,
      #eef7ff 100%
    );
}

.login-card {
  width: 100%;
  max-width: 440px;

  background: white;

  padding: 42px;

  border-radius: 18px;

  box-shadow:
    0 20px 50px rgba(30, 64, 175, 0.12);

  border: 1px solid #e8eef8;
}




.brand-section {
  text-align: center;

  margin-bottom: 32px;
}


.logo {
  width: 64px;
  height: 64px;

  margin: 0 auto 16px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: linear-gradient(
    135deg,
    #2563eb,
    #4f46e5
  );

  border-radius: 16px;

  font-size: 30px;

  box-shadow:
    0 10px 25px rgba(37, 99, 235, 0.25);
}


.brand-section h1 {
  margin: 0;

  font-size: 28px;

  font-weight: 700;

  color: #111827;
}


.brand-section p {
  margin-top: 8px;

  margin-bottom: 0;

  font-size: 14px;

  color: #6b7280;
}




.form-group {
  margin-bottom: 20px;
}


.form-group label {
  display: block;

  margin-bottom: 8px;

  font-size: 14px;

  font-weight: 600;

  color: #374151;
}



.input-wrapper {
  position: relative;

  display: flex;

  align-items: center;
}


.input-icon {
  position: absolute;

  left: 14px;

  font-size: 16px;

  pointer-events: none;
}


.input-wrapper input {
  width: 100%;

  height: 48px;

  padding: 0 48px 0 44px;

  border: 1px solid #d1d5db;

  border-radius: 10px;

  outline: none;

  font-size: 14px;

  color: #111827;

  background: #fff;

  transition: all 0.2s ease;
}


.input-wrapper input::placeholder {
  color: #9ca3af;
}


.input-wrapper input:focus {
  border-color: #2563eb;

  box-shadow:
    0 0 0 3px rgba(37, 99, 235, 0.1);
}


.password-toggle {
  position: absolute;

  right: 12px;

  border: none;

  background: transparent;

  color: #2563eb;

  font-size: 12px;

  font-weight: 600;

  cursor: pointer;
}


.password-toggle:hover {
  color: #1d4ed8;
}



.error-message {
  padding: 12px 14px;

  margin-bottom: 20px;

  border-radius: 8px;

  background: #fef2f2;

  border: 1px solid #fecaca;

  color: #b91c1c;

  font-size: 13px;

  line-height: 1.4;
}



.login-button {
  width: 100%;

  height: 48px;

  margin-top: 6px;

  border: none;

  border-radius: 10px;

  background: linear-gradient(
    135deg,
    #2563eb,
    #4f46e5
  );

  color: white;

  font-size: 15px;

  font-weight: 600;

  cursor: pointer;

  transition: all 0.2s ease;
}


.login-button:hover:not(:disabled) {
  transform: translateY(-1px);

  box-shadow:
    0 8px 20px rgba(37, 99, 235, 0.25);
}


.login-button:active:not(:disabled) {
  transform: translateY(0);
}


.login-button:disabled {
  opacity: 0.65;

  cursor: not-allowed;
}




.register-section {
  display: flex;

  justify-content: center;

  gap: 5px;

  margin-top: 26px;

  font-size: 14px;

  color: #6b7280;
}


.register-section a {
  color: #2563eb;

  font-weight: 600;

  text-decoration: none;
}


.register-section a:hover {
  text-decoration: underline;
}


.footer {
  margin-top: 28px;

  padding-top: 18px;

  border-top: 1px solid #eef2f7;

  text-align: center;

  font-size: 11px;

  color: #9ca3af;
}



@media (max-width: 500px) {

  .login-page {
    padding: 18px;
  }

  .login-card {
    padding: 30px 22px;
  }

  .brand-section h1 {
    font-size: 24px;
  }

}

</style>