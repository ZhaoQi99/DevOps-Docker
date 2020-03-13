import { login, changePassword } from "@/api/user";

export default {
  state: {
    userName: "",
    nickName: "",
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
      localStorage.token = token;
    },
    setHasGetInfo(state, status) {
      state.hasGetInfo = status;
    },
    setRules(state, rules) {
      state.rules = rules;
    },
    setNickName(state, nickName) {
      state.nickName = nickName;
    }
  },
  actions: {
    handleLogin({ commit }, { username, password }) {
      username = username.trim();
      password = password.trim();
      return new Promise((resolve, reject) => {
        login({ username, password })
          .then(res => {
            const data = res.data;
            commit("setToken", data.token);
            // commit("setUserName", res.username);
            commit("setUserId", data.user_id);
            commit("setNickName", data.nick_name);
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
        changePassword(data)
          .then(() => {
            this.$Message.success(this.$i18n.t("Change password success"));
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
