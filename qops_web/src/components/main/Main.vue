<template>
  <v-app>
    <ToolBar @changeDrawer="drawer = !drawer"></ToolBar>
    <Menu :drawer="drawer" :menu-list="menuList"></Menu>
    <v-content>
      <v-container fluid>
        <transition name="move" mode="out-in">
          <router-view></router-view>
        </transition>
      </v-container>
    </v-content>
    <Footer></Footer>
  </v-app>
</template>

<script>
import Menu from "./components/Menu";
import ToolBar from "./components/ToolBar";
import Footer from "./components/Footer";
export default {
  name: "main",
  data() {
    return {
      drawer: false,
      menuList: [
        {
          to: "/login",
          icon: "mdi-view-dashboard",
          text: "测试登录"
        },
        {
          to: "/dashboard",
          icon: "mdi-speedometer",
          text: "仪表盘"
        },
        {
          icon: "mdi-settings",
          text: "系统管理",
          children: [
            {
              to: "/account/user",
              icon: "mdi-account",
              text: "用户管理"
            },
            {
              to: "/account/role",
              icon: "mdi-account-multiple",
              text: "角色管理"
            }
          ]
        }
      ]
    };
  },
  components: {
    Menu,
    ToolBar,
    Footer
  }
};
</script>
