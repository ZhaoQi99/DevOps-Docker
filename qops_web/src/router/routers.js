import error from "./error";
import Main from "@/components/main";
import Dashboard from "@/views/dashboard";

export const routerMap = [
  {
    path: "/system",
    name: "systemManage",
    meta: {
      icon: "ios-settings",
      title: "系统管理",
      hideInMenu: false
    },
    component: Main,
    children: [
      {
        path: "permission",
        name: "permissionManage",
        meta: {
          icon: "ios-lock",
          title: "权限管理"
        },
        component: () => import("@/views/system-manage/permission.vue")
      },
      {
        path: "menu",
        name: "menuManage",
        meta: {
          icon: "ios-menu",
          title: "菜单管理"
        },
        component: () => import("@/views/system-manage/menu.vue")
      },
      {
        path: "role",
        name: "roleManage",
        meta: {
          icon: "md-people",
          title: "角色管理"
        }
        // component: () => import("@/view/system-manage/role.vue")
      },
      {
        path: "user",
        name: "userManage",
        meta: {
          icon: "md-person",
          title: "用户管理"
        },
        component: () => import("@/views/system-manage/user.vue")
      }
    ]
  },
  {
    path: "/",
    name: "home",
    component: Main,
    meta: {
      hideInMenu: false,
      icon: "md-home"
    },
    children: [
      {
        path: "/host",
        name: "hostManage",
        meta: {
          icon: "ios-card-outline",
          title: "主机管理"
        },
        component: () => import("@/views/host/hosts.vue")
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
          icon: "ios-desktop",
          title: "工作台",
          hideInMenu: false
        }
      }
    ]
  },
  {
    path: "/github",
    name: "Github",
    meta: {
      title: "官方文档",
      href: "https://github.com/ZhaoQi99/DevOps-Docker",
      icon: "logo-github"
    }
  },
  ...error
];
