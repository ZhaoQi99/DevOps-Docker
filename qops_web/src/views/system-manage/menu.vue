<template>
  <div style="height:100%">
    <!-- <Row :gutter="16">
      <Col span="12"> -->
    <Card>
      <div class="search-con search-con-top">
        <Select v-model="searchKey" class="search-col">
          <Option
            v-for="item in optionColumns"
            :value="item.key"
            :key="`search-col-${item.key}`"
            >{{ item.title }}</Option
          >
        </Select>
        <Input
          clearable
          placeholder="输入关键字搜索"
          class="search-input"
          v-model="searchValue"
        />
        <Button @click="handleSearch" class="search-btn" type="primary"
          >搜索</Button
        >
        <slot name="new_btn"
          ><Button
            type="primary"
            @click="editModal('', false)"
            class="search-btn"
            >新建</Button
          ></slot
        >
      </div>
      <Table
        :height="700"
        searchable
        search-place="top"
        :data="tableData"
        :columns="columns"
        :loading="loading"
      >
        <template slot-scope="{ row }" slot="parent"
          >{{ menuDict[row.parent] }}
        </template>
        <template slot-scope="{ row }" slot="action">
          <Button
            type="primary"
            size="small"
            style="margin-right: 5px"
            @click="editModal(row, true)"
            >{{ $t("edit") }}</Button
          >
          <Button type="error" size="small" @click="handleDelete(row)">{{
            $t("delete")
          }}</Button>
        </template>
      </Table>
    </Card>
    <!-- </Col>
    </Row> -->
    <Modal
      v-model="modalVisible"
      :title="modalTitle"
      :loading="true"
      :footer-hide="true"
    >
      <form-group
        :list="formList"
        @on-submit-success="handleSubmit"
      ></form-group>
    </Modal>
  </div>
</template>

<script>
import FormGroup from "@/components/form-group";
import { listMenu, deleteMenu, createMenu, updateMenu } from "@/api/user";
export default {
  components: {
    FormGroup
  },
  computed: {
    modalTitle() {
      if (this.editModalData) {
        return "编辑菜单";
      } else {
        return "新建菜单";
      }
    },
    optionColumns() {
      let ret = [];
      for (let item of this.columns) {
        if (item.key !== "action") {
          ret.push(item);
        }
      }
      return ret;
    }
  },
  data() {
    return {
      modalVisible: false,
      searchValue: "",
      searchKey: "",
      loading: false,
      tableData: [],
      formList: [],
      editModalData: "",
      columns: [
        { title: "菜单名称", key: "name", minWidth: 200, sortable: false },
        { title: "菜单Key", key: "key", minWidth: 200, sortable: false },
        {
          title: "父菜单名称",
          key: "parent",
          slot: "parent",
          minWidth: 200,
          sortable: false
        },
        {
          title: "操作",
          key: "action",
          slot: "action",
          width: 150
        }
      ],
      menuDict: {}
    };
  },
  methods: {
    // 获取菜单列表
    getMenusList(key, value) {
      let params = {};
      this.loading = true;
      params[key] = value;
      listMenu(params)
        .then(res => {
          this.tableData = res.data.list;
          this.loading = false;
          this.menuDict = {};
          for (let item of res.data.list) {
            this.menuDict[item.id] = item.name;
          }
        })
        .catch(() => {
          this.loading = true;
        });
    },
    // 添加 修改
    handleSubmit(value) {
      if (this.editModalData) {
        updateMenu(value.data).then(() => {
          this.$Message.success(this.$i18n.t("update success"));

          this.getMenusList();
          this.modalVisible = false;
        });
      } else {
        delete value.data.id;
        createMenu(value.data).then(() => {
          this.$Message.success(this.$i18n.t("create success"));
          this.getMenusList();
          this.modalVisible = false;
        });
      }
    },
    // 弹出对话框
    editModal(row, edit) {
      this.modalVisible = true;
      this.editModalData = edit;
      let tempList = [];
      for (let item of this.tableData) {
        tempList.push({ value: item.id, title: item.name });
      }
      this.formList = [
        {
          name: "obj_id",
          value: edit === true ? row.id : ""
        },
        {
          name: "name",
          type: "i-input",
          value: edit === true ? row.name : "",
          label: "菜单名称",
          rule: [{ required: true, message: "名称不能为空", trigger: "blur" }]
        },
        {
          name: "key",
          type: "i-input",
          value: edit === true ? row.key : "",
          label: "菜单Key",
          rule: [{ required: true, message: "Key不能为空", trigger: "blur" }]
        },
        {
          name: "parent",
          type: "i-select",
          value: edit === true ? row.parent : "",
          label: "父菜单名称",
          children: {
            type: "i-option",
            list: tempList
          }
        }
      ];
    },
    // 删除
    handleDelete(row) {
      this.$Modal.confirm({
        title: this.$i18n.t("Confirm delete"),
        content: this.$i18n.t("Are you sure you want to delete {msg} ?", {
          msg: row.name
        }),
        loading: true,
        onOk: () => {
          deleteMenu({ obj_id: row.id })
            .then(() => {
              this.$Message.success(this.$i18n.t("delete success"));
              this.tableData.splice(row._index, 1);
              this.$Modal.remove();
            })
            .catch(() => {
              this.$Modal.remove();
            });
        },
        onCancel: () => {
          this.$Message.info(this.$i18n.t("cancel"));
        }
      });
    },
    handleSearch() {
      this.getMenusList(this.searchKey, this.searchValue);
    }
  },
  mounted() {
    this.getMenusList();
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
