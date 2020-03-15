<template>
  <div style="height:100%">
    <Card>
      <div class="search-con search-con-top">
        <Select
          clearable
          v-model="searchKey"
          class="search-col"
          placeholder="主机类别"
        >
          <Option
            v-for="item in categorys"
            :value="item.value"
            :key="`search-col-${item.value}`"
            >{{ item.label }}</Option
          >
        </Select>
        <Button
          type="primary"
          @click="handleEdit('', false)"
          class="search-btn"
          >{{ $t("new") }}</Button
        >
      </div>
      <Table
        :columns="columns"
        :data="filterHosts"
        :loading="loading"
        search-place="top"
      >
        <template slot-scope="{ row }" slot="action">
          <Button
            type="primary"
            size="small"
            style="margin-right: 5px"
            @click="handleEdit(row, true)"
            >{{ $t("edit") }}</Button
          >
          <Button type="error" size="small" @click="handleDelete(row)">{{
            $t("delete")
          }}</Button>
          <Button type="info" size="small" @click="handleConsole(row)">{{
            $t("console")
          }}</Button>
        </template></Table
      >
    </Card>
    <Modal
      v-model="modalVisible"
      :title="modalTitle"
      :loading="loading2"
      :footer-hide="true"
      width="40%"
    >
      <Form :list="formList" @on-submit-success="handleSubmit"></Form>
    </Modal>
  </div>
</template>

<script>
import { listHost, createHost, updateHost, deleteHost } from "@/api/host";
import Form from "./components/form";
export default {
  components: {
    Form
  },
  data() {
    return {
      hosts: [],
      categorys: [],
      columns: [
        { title: "ID", key: "id", sortable: false },
        {
          title: "类别",
          key: "category",
          sortable: false
        },
        { title: "主机名称", key: "name", sortable: false },
        { title: "主机地址", key: "hostname", sortable: false, minWidth: 200 },
        { title: "端口", key: "port", sortable: false },
        { title: "备注", key: "desc", sortable: false },
        {
          title: "操作",
          key: "port",
          slot: "action",
          sortable: false,
          minWidth: 200,
          align: "center"
        }
      ],
      loading: false,
      searchKey: "",
      // edit form
      modalVisible: false,
      loading2: false,
      edit: false,
      formList: []
    };
  },
  computed: {
    filterHosts() {
      if (this.searchKey != "" && this.searchKey != undefined) {
        return this.hosts.filter(x => x.category == this.searchKey);
      }
      return this.hosts;
    },
    modalTitle() {
      if (this.edit) {
        return "编辑主机";
      } else {
        return "新建主机";
      }
    }
  },
  methods: {
    getHostList() {
      this.loading = true;
      listHost()
        .then(res => {
          this.hosts = res.data.hosts;
          this.categorys = [];
          for (let item of res.data.categorys) {
            this.categorys.push({ label: item, value: item });
          }
          this.columns[1].filters = this.categorys;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    handleEdit(row, edit) {
      this.edit = edit;
      this.modalVisible = true;
      this.formList = [
        {
          name: "obj_id",
          value: edit === true ? row.id : ""
        },
        {
          name: "category",
          type: "i-select",
          value: edit === true ? row.category : "",
          label: "主机类别",
          multiple: true,
          children: Object.assign([], this.categorys),
          rule: [
            { required: true, message: "主机类别不能为空", trigger: "change" }
          ],
          placeholder: "请选择主机类别"
        },
        {
          name: "name",
          type: "i-input",
          value: edit === true ? row.name : "",
          label: "主机名称",
          rule: [
            { required: true, message: "主机名称不能为空", trigger: "blur" }
          ],
          placeholder: "请输入主机名称"
        },
        {
          name: "username",
          type: "username",
          value: edit === true ? row.username : "",
          label: "连接地址",
          // label: "用户名",
          rule: [
            { required: true, message: "用户名不能为空", trigger: "blur" }
          ],
          placeholder: "用户名"
        },
        {
          name: "hostname",
          type: "",
          value: edit === true ? row.hostname : "",
          // label: "主机地址",
          rule: [
            { required: true, message: "主机地址不能为空", trigger: "blur" }
          ],
          placeholder: "主机名/IP"
        },
        {
          name: "port",
          type: "",
          value: edit === true ? row.port : "",
          // label: "主机端口",
          rule: [
            {
              required: true,
              type: "integer",
              message: "端口不能为空",
              trigger: "blur"
            },
            {
              type: "integer",
              range: [1, 65535],
              message: "端口号必须在1~65535之间",
              trigger: "blur"
            }
          ],
          placeholder: "端口"
        },
        {
          name: "desc",
          type: "textarea",
          value: edit === true ? row.desc : "",
          label: "备注信息",
          rule: [],
          placeholder: "请输入备注信息"
        }
      ];
    },
    handleDelete(row) {
      this.$Modal.confirm({
        title: this.$i18n.t("Confirm delete"),
        content: this.$i18n.t("Are you sure you want to delete {msg} ?", {
          msg: row.name
        }),
        loading: true,
        onOk: () => {
          deleteHost({ obj_id: row.id })
            .then(() => {
              this.$Message.success(this.$i18n.t("delete success"));
              this.tableData.splice(row._index, 1);
              this.$Modal.remove();
            })
            .catch(() => {
              this.$Modal.remove();
            });
          this.getHostList();
        },
        onCancel: () => {
          this.$Message.info(this.$i18n.t("cancel"));
        }
      });
    },
    handleSubmit(value) {
      if (this.edit) {
        updateHost(value.data).then(() => {
          this.$Message.success(this.$i18n.t("update success"));
          this.modalVisible = false;
          this.getHostList();
        });
      } else {
        delete value.data.obj_id;
        createHost(value.data).then(() => {
          this.$Message.success(this.$i18n.t("create success"));
          this.getHostList();
          this.modalVisible = false;
        });
      }
    },
    handleConsole(row) {
      console.log(row);
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
