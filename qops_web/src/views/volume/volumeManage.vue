<template>
  <div style="height:100%">
    <selectHost :datetime="datetime" @host-change="getVolumeList"></selectHost>
    <Card>
      <Table :columns="columns" :data="data">
        <template slot-scope="{}" slot="action">
          <Button type="error" size="small">{{ $t("delete") }}</Button>
        </template>
      </Table>
    </Card>
  </div>
</template>

<script>
import selectHost from "@/components/host/selectHost.vue";
import { listVolume } from "@/api/docker";

export default {
  components: {
    selectHost
  },
  data() {
    return {
      loading: false,
      data: [],
      columns: [
        {
          title: "ID",
          key: "short_id",
          sortable: true,
          tooltip: true,
          align: "center"
        },
        {
          title: "挂载名",
          key: "name",
          sortable: true,
          minWidth: 200,
          tooltip: true,
          align: "center"
        },
        {
          title: "Driver",
          key: "driver",
          sortable: false,
          maxWidth: 120,
          align: "center"
        },
        {
          title: "挂载点",
          key: "mount_point",
          sortable: false,
          minWidth: 130,
          tooltip: true,
          align: "center"
        },
        {
          title: "创建时间",
          key: "created",
          align: "center",
          sortable: true
        },
        {
          title: "操作",
          key: "action",
          slot: "action",
          align: "center",
          sortable: false,
          maxWidth: 100
        }
      ],
      datetime: ""
    };
  },
  methods: {
    getVolumeList(data) {
      this.loading = true;
      this.datetime = "";
      listVolume(data)
        .then(res => {
          this.loading = false;
          this.data = res.data.list;
          this.datetime = res.data.datetime;
        })
        .catch(() => {
          this.loading = false;
        });
    }
  }
};
</script>

<style lang="" scoped></style>
