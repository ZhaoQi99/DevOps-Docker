import {
  getBreadCrumbList,
  getHomeRoute,
  localSave,
  localRead
} from "@/libs/util";
import { routes } from "@/router/routers";

import config from "@/config";
const { homeName } = config;

export default {
  state: {
    breadCrumbList: [],
    homeRoute: getHomeRoute(routes, homeName),
    local: localRead("local")
  },
  getters: {},
  mutations: {
    setBreadCrumb(state, route) {
      state.breadCrumbList = getBreadCrumbList(route, state.homeRoute);
    },
    setLocal(state, lang) {
      localSave("local", lang);
      state.local = lang;
    }
  },
  actions: {}
};
