<style lang="less">
@import "./login.less";
</style>

<template>
  <div class="login">
    <div class="login-con">
      <Card icon="log-in" title="欢迎登录QOps容器管理平台" :bordered="false">
        <div class="form-con">
          <login-form @on-success-valid="handleSubmit"></login-form>
          <p class="login-tip">支持 本地 LDAP登录</p>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
import { LoginForm } from "@/components/login-form";
import { mapActions } from "vuex";
export default {
  components: {
    LoginForm
  },
  data() {
    return {};
  },

  methods: {
    ...mapActions(["handleLogin"]),
    handleSubmit({ username, password, type }) {
      const nextUrl = this.$route.query.next ? this.$route.query.next : "/";

      this.handleLogin({ username, password,type })
        .then(() => {
          this.$Message.success({
            content: this.$i18n.t("Login Success"),
            duration: 5,
            closable: true
          });
          this.$router.push(nextUrl);
        })
        .catch(() => {});
    }
  }
};
</script>

<style></style>
