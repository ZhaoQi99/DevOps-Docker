import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import ViewUI from "view-design";
import "view-design/dist/styles/iview.css";

Vue.config.productionTip = false;
Vue.use(ViewUI, {
  i18n: function(path, options) {
    let value = i18n.t(path, options);
    if (value !== null && value !== undefined) {
      return value;
    }
    return "";
  }
  // transfer: true,
  // size: "large"
});
import i18n from "@/locale";
import config from "@/config";

Vue.prototype.$config = config;
new Vue({
  router,
  store,
  i18n,
  render: function(h) {
    return h(App);
  }
}).$mount("#app");
