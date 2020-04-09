<template>
  <Layout style="height: 100%" class="main">
    <Sider
      hide-trigger
      collapsible
      :width="230"
      :collapsed-width="64"
      breakpoint="xl"
      v-model="collapsed"
      class="left-sider"
      :style="{ overflow: 'hidden' }"
    >
      <side-menu
        accordion
        ref="sideMenu"
        :active-name="$route.name"
        :collapsed="collapsed"
        @on-select="turnToPage"
        :menu-list="menuList"
      >
        <!-- 需要放在菜单上面的内容，如Logo，写在side-menu标签内部，如下 -->
        <div class="logo-con">
          <img
            v-show="!collapsed"
            style="width:120px; height:60px; border-radius:5px 5px 5px 0; margin-left: 20px;"
            :src="maxLogo"
            key="max-logo"
          />
          <img v-show="collapsed" :src="minLogo" key="min-logo" />
        </div>
      </side-menu>
    </Sider>
    <Layout>
      <Header class="header-con">
        <header-bar
          :collapsed="collapsed"
          @on-coll-change="handleCollapsedChange"
        >
          <user :user-avator="userAvator" :nick-name="nickName" />
          <language
            v-if="$config.useI18n"
            @on-lang-change="setLocal"
            style="margin-right: 10px;"
            :lang="local"
          />
          <fullscreen v-model="isFullscreen" style="margin-right: 10px;" />
        </header-bar>
      </Header>
      <Content class="main-content-con">
        <Layout class="main-layout-con">
          <Content class="content-wrapper">
            <router-view />
          </Content>
        </Layout>
      </Content>
      <copyRight></copyRight>
    </Layout>
  </Layout>
</template>
<script>
import SideMenu from "./components/side-menu";
import HeaderBar from "./components/header-bar";
import User from "./components/user";
import Fullscreen from "./components/fullscreen";
import Language from "./components/language";
import { mapMutations } from "vuex";
import minLogo from "@/assets/docker.svg";
import maxLogo from "@/assets/docker.svg";
import "./main.less";
import copyRight from "./components/footer/copyright";
export default {
  name: "Main",
  components: {
    SideMenu,
    HeaderBar,
    Language,
    Fullscreen,
    User,
    copyRight
  },
  data() {
    return {
      collapsed: false,
      minLogo,
      maxLogo,
      isFullscreen: false
    };
  },
  computed: {
    userAvator() {
      return this.$store.state.user.avatorImgPath;
    },
    nickName() {
      return this.$store.state.user.nickName;
    },
    menuList() {
      return this.$store.state.router.menuList;
    },
    local() {
      return this.$store.state.app.local;
    },
    hasReadErrorPage() {
      return this.$store.state.app.hasReadErrorPage;
    }
  },
  methods: {
    ...mapMutations(["setBreadCrumb", "setLocal"]),
    turnToPage(route) {
      let { name, params, query } = {};
      if (typeof route === "string") name = route;
      else {
        name = route.name;
        params = route.params;
        query = route.query;
      }
      if (name.indexOf("isTurnByHref_") > -1) {
        window.open(name.split("_")[1]);
        return;
      }
      this.$router.push({
        name,
        params,
        query
      });
    },
    handleCollapsedChange(state) {
      this.collapsed = state;
    },
    handleClick(item) {
      this.turnToPage(item);
    }
  },
  watch: {
    $route(newRoute) {
      // const { name, query, params, meta } = newRoute;
      this.setBreadCrumb(newRoute);
      this.$refs.sideMenu.updateOpenName(newRoute.name);
    }
  },
  mounted() {
    /**
     * @description 初始化设置面包屑导航
     */
    this.setBreadCrumb(this.$route);
    // 设置初始语言
    this.setLocal(this.$i18n.locale);
    // 获取菜单
  }
};
</script>
