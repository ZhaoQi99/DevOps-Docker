<template>
  <div class="search-con search-con-top">
    <Select
      clearable
      v-model="category"
      class="search-col"
      placeholder="主机类别"
    >
      <Option
        v-for="item in categorys"
        :value="item"
        :key="`search-col-${item}`"
        >{{ item }}</Option
      >
    </Select>
    <Select
      clearable
      v-model="host"
      class="search-col"
      placeholder="主机名"
      style="margin-left: 10px"
    >
      <Option
        v-for="item in filterHosts"
        :value="item.id"
        :key="`search-col-${item.id}`"
        >{{ item.name }}</Option
      >
    </Select>
    <Button style="margin-left: 10px" type="primary" @click="refresh">{{
      $t("refresh")
    }}</Button>
    <Span style="margin-left: 10px" v-if="datetime"
      >{{ $t("update time") }}: {{ datetime }}</Span
    >
  </div>
</template>

<script>
import { listHost } from "@/api/host";

export default {
  name: "",
  props: {
    datetime: {
      type: String,
      default: () => {
        return "";
      }
    }
  },
  computed: {
    filterHosts() {
      return this.hosts.filter(x => x.category == this.category);
    }
  },
  watch: {
    category() {
      //set default host
      let tempList = this.filterHosts.filter(
        x => x.category != "" && x.category != null
      );
      if (tempList.length > 0) {
        this.host = tempList[0].id;
      }
    },
    host(newVal) {
      let data = {
        host_id: newVal
      };
      this.$emit("host-change", data);
    }
  },
  data() {
    return {
      hosts: [],
      categorys: [],
      host: "",
      category: ""
    };
  },
  methods: {
    getHostList() {
      listHost().then(res => {
        this.hosts = res.data.hosts;
        this.categorys = res.data.categorys;
        // set default
        if (this.categorys.length > 0) {
          this.category = this.categorys[0];
        }
      });
    },
    refresh() {
      let data = {
        host_id: this.host,
        refresh: true
      };
      this.$emit("host-change", data);
    }
  },
  mounted() {
    this.getHostList();
  }
};
</script>
<style lang="less" scoped>
.search-con {
  padding: 10px 0;
  .search {
    &-col {
      display: inline-block;
      width: 200px;
    }
    &-input {
      display: inline-block;
      width: 200px;
      margin-left: 2px;
    }
    &-btn {
      margin-left: 2px;
    }
  }
}
</style>
