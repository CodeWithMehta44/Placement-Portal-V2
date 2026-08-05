<template>
  <div class="container">

    <div class="login-box">

      <h1>Placement Portal</h1>
      <h2>Login</h2>

      <input
      type="email"
      placeholder="Enter Email"
      v-model="email"
      />

      <input
      type="password"
      placeholder="Enter Password"
      v-model="password"
      />

      <button @click="showData">
      Login
      </button>

      <p>
        Don't have an account?
        <router-link to="/register">
          Register
        </router-link>
      </p>

    </div>

  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref } from "vue";
import api from "../services/app";

const router = useRouter();

const email = ref("");
const password = ref("");

async function showData() {
    try {
        const response = await api.post("/login", {
            email: email.value,
            password: password.value
        });

        console.log("Login Success", response.data);
        
        // Save JWT token
        localStorage.setItem("token", response.data.access_token);
        localStorage.setItem("role", response.data.user.role);

        // Get user role
        const role = response.data.user.role;

        // Redirect based on role
        if (role === "admin") {
            router.push("/admin");
        }
        else if (role === "company") {
            router.push("/company");
        }
        else {
            router.push("/student");
        }
          } catch (error) {
            console.log(error);
}
}
</script>

<style scoped>

.container{
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
    background:#f2f2f2;
}

.login-box{

    width:350px;
    background:white;
    padding:30px;
    border-radius:10px;

    box-shadow:0px 0px 10px rgba(0,0,0,0.2);

    text-align:center;
}

input{

    width:100%;
    padding:10px;
    margin-top:15px;
    box-sizing:border-box;
}

button{

    width:100%;
    margin-top:20px;
    padding:10px;

    background:#007bff;
    color:white;

    border:none;
    cursor:pointer;
}

button:hover{

    background:#0056b3;
}

p{

    margin-top:20px;
}

</style>