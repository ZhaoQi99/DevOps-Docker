import axios from "axios";
import router from "../router";
import { Message, MessageBox } from "element-ui";
const service = axios.create({
  baseURL: "/api",
  timeout: 3000,
  headers: { "Content-Type": "application/json;charset=UTF-8" }
  // headers['Content-Type']: 'application/x-www-form-urlencoded;charset=UTF-8'
});

// request
service.interceptors.request.use(
  config => {
    if (localStorage.Token !== undefined) {
      config.headers["Authorization"] = "Bearer" + " " + localStorage.Token;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

//返回状态判断
service.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.status === 200 || response.status === 204) {
      return res;
    } else if (res.status === 1002 || res.status === 1001) {
      MessageBox.alert("由于用户长时间未操作,请重新登录!", "错误提示", { type: "warning" }).then(() => {
        router.replace({
          path: "/login",
          query: { redirect: router.currentRoute.fullPath }
        });
        localStorage.clear();
      });
      return new Promise(() => {});
    } else {
      // can user a table{status:type} in the future
      Message({
        message: res.message || 'Error',
        type: "error"
      });
      return Promise.reject(new Error(res.message || 'Error'));
      // return new Promise(() => {});
    }
  },
  (error) => {
    if (error.response.status === 500) {
      Message({
        message: "服务器内部错误!",
        type: "error"
      });
    } else {
      Message({
        message: error.message,
        type: "error"
      });
    return Promise.reject(error);
  }
);
export default service;
