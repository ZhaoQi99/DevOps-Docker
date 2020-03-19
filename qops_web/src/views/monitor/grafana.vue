<template>
  <iframe
    :src="url"
    frameborder="0"
    align="left"
    width="100%"
    height="100%"
    marginWidth="0"
    marginHeight="0"
    class="iframesty"
  >
    <p class="tip">你的浏览器不支持iframe标签</p>
  </iframe>
</template>

<script>
import { getSetting } from "@/api/setting";
export default {
  name: "",
  data() {
    return {
      url: ""
    };
  },
  methods: {
    getUrl() {
      let data = {
        key: "grafana_url"
      };
      getSetting(data).then(res => {
        this.url = res.data;
      });
    }
  },
  mounted() {
    this.getUrl();
  }
};
</script>

<style lang="" scoped></style>
