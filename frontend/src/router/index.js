import { createRouter, createWebHistory } from "vue-router";

import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import StudentDashboard from "../views/StudentDashboard.vue";
import CompanyDashboard from "../views/CompanyDashboard.vue";
import AdminDashboard from "../views/AdminDashboard.vue";
import CompanyJobDetails from "../views/CompanyJobDetails.vue"
import JobDetails from "../views/JobDetails.vue";
import CompanyProfile from "../views/CompanyProfile.vue";
import StudentProfile from "../views/StudentProfile.vue";

const routes = [

  {
    path: "/student/profile",
    component: StudentProfile,
    meta:{
        requiresAuth:true,
        role:"student"
    }
},
  {
    path: "/company/profile",
    component: CompanyProfile
},
  {
    path: "/company/job/:id/applications",
    component: () => import("../views/ApplicantList.vue")
},
  {
    path: "/company/create-job",
    component: () => import("../views/CreateJob.vue")
},
  {
    path: "/student/job/:id",
    component: JobDetails
},
  {
    path: "/company/job/:id",
    component: CompanyJobDetails
},
  {
    path: "/",
    component: Login,
  },
  {
    path: "/register",
    component: Register,
  },
  {
    path: "/student",
    component: StudentDashboard,
    meta: {
      requiresAuth: true,
      role: "student",
    },
  },
  {
    path: "/company",
    component: CompanyDashboard,
    meta: {
      requiresAuth: true,
      role: "company",
    },
  },
  {
    path: "/admin",
    component: AdminDashboard,
    meta: {
      requiresAuth: true,
      role: "admin",
    },
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {

    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    // Public routes
    if (!to.meta.requiresAuth) {
        return next();
    }

    // User not logged in
    if (!token) {
        return next("/");
    }

    // Wrong role
    if (to.meta.role !== role) {

        if (role === "admin") {
            return next("/admin");
        }

        if (role === "student") {
            return next("/student");
        }

        if (role === "company") {
            return next("/company");
        }

        return next("/");
    }

    next();

});

export default router;