import Vue from "vue";
import VueRouter from "vue-router";
import { routes } from "./routers";
import ViewUI from "view-design";
import { setTitle } from "@/libs/util";

Vue.use(VueRouter);

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});
router.beforeEach((to, from, next) => {
  to.meta.title && setTitle(to.meta.title);
  ViewUI.LoadingBar.start();
  console.log(from);
  next();
});
router.afterEach(to => {
  ViewUI.LoadingBar.finish();
  window.scrollTo(0, 0);
  console.log(to);
});
export default router;
