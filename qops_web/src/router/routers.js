import error from "./error";
import Main from "@/components/main";
import Dashboard from "@/views/dashboard";

export const routerMap = [
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
          icon: "ios-list-box-outline"
        },
        component: () => import("@/views/host/hosts.vue")
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
        path: "/container",
        name: "containerManage",
        meta: {
          icon: "ios-cube-outline"
        },
        component: () => import("@/views/container/containerManage.vue")
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
        path: "/image",
        name: "imageManage",
        meta: {
          icon: "ios-card-outline"
        },
        component: () => import("@/views/image/imageManage.vue")
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
        path: "/volume",
        name: "volumeManage",
        meta: {
          icon: "ios-folder-outline"
        },
        component: () => import("@/views/volume/volumeManage.vue")
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
        path: "/network",
        name: "networkManage",
        meta: {
          icon: "ios-git-network"
        },
        component: () => import("@/views/network/networkManage.vue")
      }
    ]
  },
  {
    path: "/monitor",
    name: "monitorCenter",
    component: Main,
    meta: {
      hideInMenu: false,
      icon: "ios-pulse",
      showAlways: true
    },
    children: [
      {
        path: "/host",
        name: "hostMonitor",
        meta: {
          icon: "ios-podium"
        }
        // component: () => import("@/views/network/networkManage.vue")
      },
      {
        path: "/grafana",
        name: "grafanaMonitor",
        meta: {
          icon: "ios-podium"
        },
        component: () => import("@/views/monitor/grafana.vue")
      }
    ]
  },
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
          icon: "ios-menu"
        },
        component: () => import("@/views/system-manage/menu.vue")
      },
      {
        path: "role",
        name: "roleManage",
        meta: {
          icon: "md-people"
        }
        // component: () => import("@/view/system-manage/role.vue")
      },
      {
        path: "user",
        name: "userManage",
        meta: {
          icon: "md-person"
        },
        component: () => import("@/views/system-manage/user.vue")
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
