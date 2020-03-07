import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ViewUI from "view-design";
import "view-design/dist/styles/iview.css";

Vue.config.productionTip = false;
Vue.use(ViewUI);
import i18n from "@/locale";
import config from "@/config";

Vue.prototype.$config = config;
new Vue({
  router,
  el: "#app",
  store,
  i18n,
  render: function(h) {
    return h(App);
  }
});
