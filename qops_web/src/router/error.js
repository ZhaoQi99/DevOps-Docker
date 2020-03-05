import Error404 from "@/views/error/404.vue";

export default [
  {
    path: "/error/404",
    component: Error404
  },
  {
    path: "*",
    redirect: "/error/404"
  }
];
