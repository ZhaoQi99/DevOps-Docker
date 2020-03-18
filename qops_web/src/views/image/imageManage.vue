<template>
  <div style="height:100%">
    <selectHost :datetime="datetime" @host-change="getImageList"></selectHost>
    <Card>
      <Table :columns="columns" :data="data" :loading="loading">
        <template slot-scope="{ row }" slot="tags">
          <Tag
            type="blue"
            v-for="(item, index) in row.tags"
            :key="`tag_${index}`"
            >{{ item }}</Tag
          >
        </template>
        <template slot-scope="{ row }" slot="labels">
          <Tag
            type="blue"
            v-for="(value, key) in row.labels"
            :key="`label_${key}`"
            >{{ key }}:{{ value }}</Tag
          >
        </template>
        <template slot-scope="{}" slot="action">
          <Button type="error" size="small"> {{ $t("delete") }}</Button>
        </template>
      </Table>
    </Card>
  </div>
</template>

<script>
import selectHost from "@/components/host/selectHost.vue";
import { listImage } from "@/api/docker";
export default {
  name: "",
  components: {
    selectHost
  },
  data() {
    return {
      datetime: "",
      loading: true,
      data: [],
      columns: [
        { title: "镜像Id", key: "short_id", sortable: true, align: "center" },
        {
          title: "镜像标签",
          key: "tags",
          slot: "tags",
          sortable: false,
          align: "center"
        },
        {
          title: "镜像Label",
          key: "labels",
          slot: "labels",
          sortable: false,
          align: "center",
          minWidth: 150
        },
        {
          title: "镜像大小",
          key: "size",
          sortable: true,
          align: "center"
        },
        {
          title: "创建时间",
          key: "created",
          align: "center",
          sortable: true,
          minWidth: 60
        },
        {
          title: "操作",
          key: "action",
          slot: "action",
          sortable: false,
          align: "center"
        }
      ]
    };
  },
  methods: {
    getImageList(data) {
      this.datetime = "";
      this.loading = true;
      listImage(data)
        .then(res => {
          this.data = res.data.list;
          this.datetime = res.data.datetime;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    }
  }
};
</script>

<style lang="scss" scoped></style>
