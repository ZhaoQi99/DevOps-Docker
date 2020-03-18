import { routes, routerMap } from "@/router/routers";
import { getMenuByRouter } from "@/libs/util";
// import router from "@/router";
const state = {
  routers: routes,
  hasGetRules: false,
  menuList: []
};

// const getters = {
//   menuList: state => getMenuByRouter(state.routers, "all")
// };
const mutations = {
  CONCAT_ROUTES(state, routerList) {
    state.routers = routes.concat(routerList);
    state.hasGetRules = true;
    // router.addRoutes(routerList);
    state.menuList = getMenuByRouter(state.routers, "all");
  }
};

const getAccesRouterList = (routes, rules) => {
  return routes.filter(item => {
    if (rules[item.name]) {
      if (item.children)
        item.children = getAccesRouterList(item.children, rules);
      return true;
    } else return false;
  });
};

const actions = {
  concatRoutes({ commit }, rules) {
    return new Promise((resolve, reject) => {
      try {
        let routerList = [];
        // 如果全部是true 直接返回
        if (Object.entries(rules).every(item => item[1])) {
          routerList = routerMap;
        } else {
          routerList = getAccesRouterList(routerMap, rules);
        }

        commit("CONCAT_ROUTES", routerList);
        resolve(routerList);
      } catch (err) {
        reject(err);
      }
    });
  }
};

export default {
  state,
  mutations,
  actions
};
