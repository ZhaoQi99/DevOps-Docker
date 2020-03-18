<template>
  <div style="height:100%">
    <selectHost :datetime="datetime" @host-change="getNetworkList"></selectHost>
    <Card>
      <Table :columns="columns" :data="data" :loading="loading">
        <template slot-scope="{}" slot="action">
          <Button type="error" size="small"> {{ $t("delete") }}</Button>
        </template>
      </Table>
    </Card>
  </div>
</template>

<script>
import selectHost from "@/components/host/selectHost.vue";
import { listNetwork } from "@/api/docker";

export default {
  components: {
    selectHost
  },
  data() {
    return {
      datetime: "",
      loading: true,
      data: [],
      columns: [
        {
          title: "Name",
          key: "name",
          align: "center",
          sortable: true
        },
        {
          title: "Scope",
          key: "scope",
          align: "center",
          sortable: true
        },
        {
          title: "Driver",
          key: "driver",
          align: "center",
          sortable: true
        },
        {
          title: "Attachable",
          key: "attachable",
          align: "center",
          sortable: true
        },
        {
          title: "Ipam Driver",
          key: "ipam_driver",
          align: "center",
          sortable: true
        },
        {
          title: "IPam Subnet",
          key: "ipam_subnet",
          align: "center",
          sortable: true
        },
        {
          title: "Ipam Gateway",
          key: "ipam_gateway",
          align: "center",
          sortable: true
        },
        {
          title: "操作",
          key: "action",
          slot: "action",
          align: "center",
          sortable: true
        }
      ]
    };
  },
  methods: {
    getNetworkList(data) {
      this.datetime = "";
      this.loading = true;
      listNetwork(data)
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

<style scoped></style>
