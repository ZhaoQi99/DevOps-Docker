<template>
  <v-navigation-drawer
    v-model="inputValue"
    app
    :expand-on-hover="expandOnHover"
    floating
  >
    <v-toolbar color="primary" dark>
      <v-toolbar-title class="ml-0 pl-3" v-if="!drawer">
        <span>QOps 容器管理平台</span>
      </v-toolbar-title>
    </v-toolbar>

    <v-divider class="mx-3 mb-3" />

    <v-list nav>
      <v-list-item>
        <v-list-item-content>
          <v-img contain src="@/assets/logo.svg" height="80"></v-img>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <template v-for="(link, i) in menuList">
        <v-list-item v-if="!link.children" :key="link.to" :to="link.to">
          <v-list-item-action>
            <v-icon>{{ link.icon }}</v-icon>
          </v-list-item-action>
          <v-list-item-title v-text="link.text"></v-list-item-title>
        </v-list-item>
        <v-list-group
          v-else-if="link.children"
          :prepend-icon="link.icon"
          no-action
          :key="i"
        >
          <template v-slot:activator>
            <v-list-item-title>{{ link.text }}</v-list-item-title>
          </template>
          <v-list-item
            v-for="child in link.children"
            :key="child.to"
            :to="child.to"
          >
            <v-list-item-title v-text="child.text" />
            <v-list-item-action>
              <v-icon v-text="child.icon"></v-icon>
            </v-list-item-action>
          </v-list-item>
        </v-list-group>
      </template>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  props: {
    drawer: {
      type: Boolean,
      default: false
    },
    menuList: {
      type: Array,
      default: () => [],
      required: true
    }
  },
  data() {
    return {
      expandOnHover: this.drawer,
      inputValue: "/"
    };
  },
  computed: {},
  methods: {},
  watch: {
    drawer(val) {
      this.expandOnHover = val;
    }
  }
};
</script>
