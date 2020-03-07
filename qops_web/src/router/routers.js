import error from "./error";
import Main from "@/components/main";
import Dashboard from "@/views/dashboard";

export const routes = [
  {
    path: "/",
    name: "home",
    component: Main,
    redirect: "/dashboard",
    meta: {
      hideInMenu: false
    },
    children: [
      {
        path: "dashboard",
        name: "dashboard",
        component: Dashboard,
        meta: {
          icon: "ios-add",
          title: "测试",
          hideInMenu: false
        }
      }
    ]
  },
  {
    path: "/doc",
    name: "doc",
    meta: {
      title: "官方文档",
      href: "http://docs.opendevops.cn/zh/latest/",
      icon: "ios-book"
    }
  },
  ...error
];
