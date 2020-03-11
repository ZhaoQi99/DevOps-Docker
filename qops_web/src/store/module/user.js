import { login, password } from "@/api/user";

export default {
  state: {
    userName: "",
    userId: "",
    avatorImgPath:
      "https://file.iviewui.com/dist/a0e88e83800f138b94d2414621bd9704.png",
    token: "",
    access: "",
    rules: {},
    hasGetInfo: false
  },
  mutations: {
    setAvator(state, avatorPath) {
      state.avatorImgPath = avatorPath;
    },
    setUserId(state, id) {
      state.userId = id;
    },
    setUserName(state, name) {
      state.userName = name;
    },
    setAccess(state, access) {
      state.access = access;
    },
    setToken(state, token) {
      state.token = token;
    },
    setHasGetInfo(state, status) {
      state.hasGetInfo = status;
    },
    setRules(state, rules) {
      state.rules = rules;
    }
  },
  actions: {
    handleLogin({ commit }, { username, password }) {
      username = username.trim();
      password = password.trim();
      return new Promise((resolve, reject) => {
        login({ username, password })
          .then(res => {
            commit("setToken", res.token);
            commit("setUserName", res.username);
            resolve(res);
          })
          .catch(err => {
            reject(err);
          });
      });
    },
    handleLogOut() {
      return new Promise(resolve => {
        localStorage.clear();

        resolve();
      });
    },
    handlePassword({ commit }, data) {
      return new Promise((resolve, reject) => {
        password(data)
          .then(() => {
            commit("setToken", "");
            commit("setAccess", []);
            resolve({});
          })
          .catch(err => {
            reject(err);
          });
      });
    }
  }
};
