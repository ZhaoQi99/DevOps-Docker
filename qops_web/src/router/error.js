import Error404 from "@/views/error/404.vue";

export default [
  {
    path: "/error/404",
    component: Error404,
    meta: {
      hideInMenu: true
    }
  },
  {
    path: "*",
    redirect: "/error/404",
    meta: {
      hideInMenu: true
    }
  }
];
