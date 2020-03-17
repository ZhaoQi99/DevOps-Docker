import Vue from "vue";
import VueRouter from "vue-router";
import { routes } from "./routers";
import ViewUI from "view-design";
import { setTitle } from "@/libs/util";
import { getSelf } from "../api/user";
import store from "@/store";
import i18n from "@/locale";
Vue.use(VueRouter);
const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});
// router.addRoutes(routerMap);
router.beforeEach((to, from, next) => {
  setTitle(i18n.t(to.name));
  ViewUI.LoadingBar.start();
  if (to.name === "login") {
    next();
  } else {
    if (!store.state.router.hasGetRules) {
      getSelf()
        .then(res => {
          const rules = res.data.menus;
          store.dispatch("concatRoutes", rules).then(routers => {
            router.addRoutes(routers);
            next(to.redirectedFrom);
          });
        })
        .catch(() => {
          next({ name: "login" });
        });
    } else {
      next();
    }
  }
});
router.afterEach(() => {
  ViewUI.LoadingBar.finish();
  window.scrollTo(0, 0);
});
export default router;
