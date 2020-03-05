<template>
  <v-footer padless>
    <v-card flat tile class="flex" color="primary">
      <v-card-text class="py-1 text-center">
        <v-btn
          v-for="(link, index) in links"
          :key="link"
          text
          class="white--text"
          :href="handles[index]"
        >
          {{ link }}
        </v-btn>
        <v-btn
          icon
          class="my-1 white--text"
          href="https://github.com/ZhaoQi99/DevOps-Docker"
        >
          <v-icon class="fa-2x">mdi-github-circle</v-icon>
        </v-btn>
        <v-divider></v-divider>
        <v-col class="primary text-center white--text py-1">
          Copyright © {{ new Date().getFullYear() }} - <strong>Qi Zhao</strong>
        </v-col>
      </v-card-text>
    </v-card>
  </v-footer>
</template>
<script>
export default {
  data: () => ({
    links: ["用户帮助", "意见反馈", "联系我们"],
    handles: ["", "", "mailto:zhaoqi99@outlook.com"]
  })
};
</script>
