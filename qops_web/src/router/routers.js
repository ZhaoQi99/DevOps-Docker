import error from "./error";
import Main from "@/components/main";
import Dashboard from "@/views/dashboard";

export const routerMap = [
  {
    path: "/userManage",
    name: "userManage",
    meta: {
      icon: "md-contacts",
      title: "用户管理",
      hideInMenu: false
    },
    component: Main,
    children: [
      {
        path: "permissions",
        name: "permissions",
        meta: {
          icon: "ios-lock",
          title: "权限列表"
        },
        component: () => import("@/views/user-manage/permission.vue")
      },
      {
        path: "menus",
        name: "menus",
        meta: {
          icon: "ios-menu",
          title: "菜单组件"
        },
        // component: () => import("@/view/user-manage/routescomponents.vue")
      },
      {
        path: "roles",
        name: "roles",
        meta: {
          icon: "ios-person",
          title: "角色管理"
        },
        // component: () => import("@/view/user-manage/role.vue")
      }
    ]
  }
];
export const routes = [
  {
    path: "/login",
    name: "login",
    meta: {
      title: "Login - 登录",
      icon: "md-home",
      hideInMenu: true
    },
    component: () => import("@/views/login/login.vue")
  },
  {
    path: "/",
    name: "home",
    component: Main,
    redirect: "/dashboard",
    meta: {
      hideInMenu: false,
      icon: "md-home"
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
