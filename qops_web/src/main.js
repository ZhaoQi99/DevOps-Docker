import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from './plugins/vuetify';
import 'roboto-fontface/css/roboto/roboto-fontface.css'
import '@mdi/font/css/materialdesignicons.css'

Vue.config.productionTip = false;

new Vue({
  router,
  el: "#app",
  vuetify,

  render: function(h) {
    return h(App);
  }
});
