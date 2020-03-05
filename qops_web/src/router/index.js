import Vue from "vue";
import VueRouter from "vue-router";
import error from "./error";
import Main from "@/components/main/Main.vue";
import Dashboard from "@/views/dashboard";
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    component: Main,
    redirect: "/dashboard",
    children: [
      {
        path: "/dashboard",
        component: Dashboard,
        meta: {
          icon: "ios-add",
          text: "测试"
        }
      }
    ]
  },
  ...error
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
