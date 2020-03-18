<template>
  <div style="height:100%">
    <selectHost
      :datetime="datetime"
      @host-change="getContainerList"
    ></selectHost>
    <Card>
      <Table :columns="columns" :data="data" :loading="loading">
        <template slot-scope="{ row }" slot="status">
          <Tag color="success" v-if="row.status === 'running'">{{
            row.status
          }}</Tag>
          <Tag color="error" v-else-if="row.status === 'exited'">{{
            row.status
          }}</Tag>
          <Tag color="warning" v-else>{{ row.status }}</Tag>
        </template>
        <template slot-scope="{ row }" slot="action">
          <ButtonGroup shape="circle" size="small">
            <Button
              type="success"
              icon="ios-play"
              :disabled="['running', 'paused'].indexOf(row.status) !== -1"
            >
            </Button>
            <Button
              type="error"
              icon="ios-square"
              :disabled="['exited', 'paused'].indexOf(row.status) !== -1"
            >
            </Button>
            <Button type="error" icon="md-close"> </Button>

            <Button
              type="primary"
              icon="ios-pause"
              :disabled="['exited', 'paused'].indexOf(row.status) !== -1"
            >
            </Button>
            <Button type="primary" icon="ios-sync"> </Button>
            <Button
              type="primary"
              icon="ios-play"
              :disabled="row.status !== 'paused'"
            >
            </Button>

            <Button type="error" icon="md-trash"> </Button>
          </ButtonGroup>
        </template>
      </Table>
    </Card>
  </div>
</template>

<script>
import { listContainer } from "@/api/docker";
import selectHost from "@/components/host/selectHost.vue";
export default {
  components: {
    selectHost
  },
  data() {
    return {
      loading: false,
      data: [],
      columns: [
        { title: "容器Id", key: "short_id", sortable: true, align: "center" },
        {
          title: "容器名",
          key: "name",
          align: "center",
          minWidth: 100,
          sortable: true
        },
        {
          title: "容器状态",
          key: "status",
          sortable: false,
          slot: "status",
          maxWidth: 110
        },
        {
          title: "IP地址",
          key: "ip_address",
          sortable: true,
          maxWidth: 110,
          align: "center"
        },
        {
          title: "命令",
          key: "cmd",
          sortable: false,
          minWidth: 130,
          maxWidth: 250,
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
          align: "center",
          minWidth: 140
        }
      ],
      // select
      datetime: ""
    };
  },
  methods: {
    getContainerList(data) {
      this.datetime = "";
      this.loading = true;
      listContainer(data)
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

<style lang="less" scoped></style>
