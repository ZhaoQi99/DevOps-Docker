import axios from "axios";
import { Message } from "view-design";
import Cookies from "js-cookie";
import { localRead } from "./util";
import router from "@/router";
class HttpRequest {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
    this.queue = {};
  }
  getInsideConfig() {
    const config = {
      baseURL: this.baseUrl,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": Cookies.get("csrftoken")
      }
    };
    return config;
  }
  destroy(url) {
    delete this.queue[url];
    if (!Object.keys(this.queue).length) {
      // Spin.hide()
    }
  }
  interceptors(instance, url) {
    // 请求拦截
    instance.interceptors.request.use(
      config => {
        config.headers["Authorization"] = "Bearer" + " " + localRead("token");
        // 添加全局的loading...
        if (!Object.keys(this.queue).length) {
          // Spin.show() // 不建议开启，因为界面不友好
        }
        this.queue[url] = true;
        return config;
      },
      error => {
        return Promise.reject(error);
      }
    );
    // 响应拦截
    instance.interceptors.response.use(
      res => {
        this.destroy(url);
        const data = res.data;
        if (res.status === 200 && data.status !== 0) {
          Message.error({
            content: data.msg,
            duration: 8,
            closable: true
          });
          return Promise.reject(new Error(data));
        }
        return res.data;
      },
      error => {
        this.destroy(url);
        if (error.response.status === 401) {
          this.queue = {};
          Message.error({
            content: `${error.response.data.msg}`,
            duration: 8,
            closable: true
          });
          if (url !== "/account/login/") {
            router.replace({
              path: "/login",
              query: { next: router.currentRoute.fullPath }
            });
          }
        } else if (error.response.status === 403) {
          Message.error({
            content: "你没有权限, 请联系管理员",
            duration: 8,
            closable: true
          });
        } else if (error.response.status === 500) {
          Message.error({
            content: "服务器内部错误",
            duration: 8,
            closable: true
          });
        } else if (error.response.status === 502) {
          Message.error({
            content: "服务器开小差了",
            duration: 8,
            closable: true
          });
        } else if (error.response.status === 400) {
          Message.error({
            content: "请求参数错误",
            duration: 8,
            closable: true
          });
        } else {
          Message.error({
            content: `${error.response.status}-错误`,
            duration: 8,
            closable: true
          });
        }
        return Promise.reject(error);
      }
    );
  }
  request(options) {
    const instance = axios.create();
    options = Object.assign(this.getInsideConfig(), options);
    this.interceptors(instance, options.url);
    return instance(options);
  }
}
export default HttpRequest;
