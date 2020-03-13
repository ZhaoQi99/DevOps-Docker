<template>
  <div style="height:100%">
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
          @on-change="handleClear"
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
        size="small"
        ref="selection"
        :columns="columns"
        :data="tableData"
        :loading="loading"
      >
        <template slot-scope="{ row }" slot="action">
          <Button
            type="primary"
            size="small"
            style="margin-right: 5px"
            @click="editModal(row, true)"
            >{{ $t("edit") }}</Button
          >
          <Button type="error" size="small" @click="handleDel(row)">{{
            $t("delete")
          }}</Button>
        </template></Table
      >

      <div style="margin: 10px;overflow: hidden">
        <div style="float: left;">
          <Page
            :total="pageTotal"
            :current="pageNum"
            :page-size="pageSize"
            :page-size-opts="[10, 15, 25, 35, 50, 100]"
            show-sizer
            show-total
            @on-change="changePage"
            @on-page-size-change="handlePageSize"
          ></Page>
        </div>
      </div>

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
    </Card>
  </div>
</template>

<script>
import FormGroup from "@/components/form-group";
import {
  listPermission,
  deletePermission,
  updatePermission,
  createPermission
} from "@/api/user";
export default {
  components: {
    FormGroup
  },
  computed: {
    optionColumns() {
      let ret = [];
      for (let item of this.columns) {
        if (item.key !== "action" && item.key !== "") {
          ret.push(item);
        }
      }
      return ret;
    },
    modalTitle() {
      if (this.editModalData === true) {
        return "编辑权限";
      } else {
        return "新建权限";
      }
    }
  },
  data() {
    return {
      columns: [
        {
          title: "权限名称",
          key: "name",
          align: "center",
          sortable: true
        },
        {
          title: "请求方法",
          key: "method"
        },
        {
          title: "请求路径",
          key: "url"
        },
        {
          title: "更新时间",
          key: "updated"
        },
        {
          title: "添加时间",
          key: "created"
        },
        {
          title: "操作",
          key: "action",
          slot: "action",
          width: 150
        }
      ],
      tableData: [],
      pageTotal: 0, // 数据总数
      pageNum: 1, // 当前页码
      pageSize: 15, // 每页条数
      loading: false,
      modalVisible: false,
      formList: [],
      editModalData: "",
      searchKey: "",
      searchValue: ""
    };
  },

  methods: {
    getFuncsList(page, limit, key, value) {
      this.loading = true;
      let params = {
        limit: limit,
        offset: (page - 1) * limit
      };
      if (key !== "") {
        params[key] = value;
      }
      listPermission(params)
        .then(res => {
          this.pageTotal = res.data.total;
          this.tableData = res.data.list;
          this.loading = false;
        })
        .catch(() => {
          this.loading = false;
        });
    },
    editModal(row, edit) {
      this.editModalData = edit;
      this.modalVisible = true;
      this.formList = [
        {
          name: "obj_id",
          value: edit === true ? row.id : ""
        },
        {
          name: "name",
          type: "i-input",
          value: edit === true ? row.name : "",
          label: "权限名称",
          rule: [
            { required: true, message: "权限名称不能为空", trigger: "blur" }
          ]
        },
        {
          name: "method",
          type: "i-select",
          value: edit === true ? row.method : "",
          label: "请求方法",
          children: {
            type: "i-option",
            list: [
              { value: "GET", title: "GET" },
              { value: "POST", title: "POST" },
              { value: "PUT", title: "PUT" },
              { value: "PATCH", title: "PATCH" },
              { value: "DELETE", title: "DELETE" },
              { value: "ALL", title: "ALL" }
            ]
          },
          rule: [
            { required: true, message: "请求方法不能为空", trigger: "blur" }
          ]
        },
        {
          name: "url",
          type: "i-input",
          maxlength: 100,
          value: edit === true ? row.url : "",
          label: "请求路径",
          rule: [{ required: true, message: "URI不能为空", trigger: "blur" }]
        }
      ];
    },
    handleSubmit(value) {
      if (this.editModalData) {
        updatePermission(value.data).then(() => {
          this.$Message.success(this.$i18n.t("update success"));
          this.getFuncsList(
            this.pageNum,
            this.pageSize,
            this.searchKey,
            this.searchValue
          );
          this.modalVisible = false;
        });
      } else {
        delete value.data.id;
        createPermission(value.data).then(() => {
          this.$Message.success(this.$i18n.t("create success"));
          this.getFuncsList(
            this.pageNum,
            this.pageSize,
            this.searchKey,
            this.searchValue
          );
          this.modalVisible = false;
        });
      }
    },
    handleDel(params) {
      this.$Modal.confirm({
        title: this.$i18n.t("Confirm delete"),
        content: this.$i18n.t("Are you sure you want to delete {msg} ?", {
          msg: params.name
        }),
        loading: true,
        onOk: () => {
          deletePermission({
            obj_id: params.id
          })
            .then(() => {
              this.$Modal.remove();
              this.$Message.success(this.$i18n.t("delete success"));
              this.tableData.splice(params._index, 1);
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
    changePage(value) {
      this.pageNum = value;
      this.getFuncsList(
        this.pageNum,
        this.pageSize,
        this.searchKey,
        this.searchValue
      );
    },
    // 每页条数
    handlePageSize(value) {
      this.pageSize = value;
      this.getFuncsList(1, this.pageSize, this.searchKey, this.searchValue);
    },
    handleClear(e) {
      if (e.target.value === "") this.tableData = this.value;
    },
    handleSearch() {
      this.pageNum = 1;
      this.getFuncsList(
        this.pageNum,
        this.pageSize,
        this.searchKey,
        this.searchValue
      );
    }
  },
  mounted() {
    this.getFuncsList(this.pageNum, this.pageSize);
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
