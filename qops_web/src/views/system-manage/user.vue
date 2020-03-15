<template>
  <div style="height:100%">
    <Card>
      <div class="search-con search-col">
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
            >{{ $t("new") }}</Button
          ></slot
        >
      </div>
      <Table :data="tableData" searchable search-place="top" :columns="columns">
        <template slot-scope="{ row }" slot="roles"
          ><Tag
            color="blue"
            :key="index"
            v-for="(name, index) in roleNameList(row.roles)"
            >{{ name }}</Tag
          >
        </template>
        <template slot-scope="{ row }" slot="action">
          <Button
            type="primary"
            size="small"
            style="margin-right: 5px"
            @click="editModal(row, true)"
            >{{ $t("edit") }}</Button
          >
          <Button
            style="margin-right: 5px"
            type="error"
            size="small"
            @click="handleDelete(row)"
            >{{ $t("delete") }}</Button
          >
          <Button type="warning" size="small" @click="handleResetPWD(row)">{{
            $t("reset password")
          }}</Button>
        </template>
      </Table>
      <div style="margin: 10px; overflow: hidden">
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
    </Card>
    <Modal
      v-model="modalVisible"
      :title="modalTitle"
      :loading="loading"
      :footer-hide="true"
    >
      <form-group
        :list="formList"
        @on-submit-success="handleSubmit"
      ></form-group>
    </Modal>
    <Modal
      v-model="resetPwdModal"
      title="重置密码"
      :loading="loading"
      :footer-hide="true"
    >
      <form-group
        :list="resetPwdformList"
        @on-submit-success="handleResetPwdSubmit"
      ></form-group>
    </Modal>
  </div>
</template>

<script>
import FormGroup from "@/components/form-group";
import {
  listUser,
  createUser,
  deleteUser,
  updateUser,
  listRole,
  resetPassword
} from "@/api/user";
export default {
  components: {
    FormGroup
  },
  computed: {
    modalTitle() {
      if (this.edit) {
        return "编辑用户";
      } else {
        return "创建用户";
      }
    },
    optionColumns() {
      let ret = [];
      for (let item of this.columns) {
        if (
          item.key !== "action" &&
          item.key !== "date_joined" &&
          item.key !== "roles"
        ) {
          ret.push(item);
        }
      }
      return ret;
    }
  },
  data() {
    return {
      resetPassword: "",
      resetPwdModal: false,
      loading: false,
      // 弹出框
      modalVisible: false,
      // 渲染form数据
      formList: [],
      columns: [
        { title: "用户名", key: "username", sortable: true, width: 100 },
        { title: "昵称", key: "nick_name", sortable: true, width: 100 },
        { title: "加入时间", key: "date_joined" },
        {
          title: "最后登录",
          key: "last_login",
          align: "center",
          sortable: true
        },
        {
          title: "角色",
          key: "roles",
          slot: "roles",
          align: "center"
        },
        {
          title: "管理员",
          key: "is_admin",
          width: 80,
          align: "center",
          render: (h, params) => {
            return h("div", [
              h("i-switch", {
                props: {
                  value: params.row.is_admin === true // 控制开关的打开或关闭状态，官网文档属性是value
                },
                style: {
                  marginRight: "5px"
                },
                on: {
                  "on-change": () => {
                    this.onSwitch(params, "is_admin");
                  }
                }
              })
            ]);
          }
        },
        {
          title: "状态",
          key: "is_active",
          width: 80,
          align: "center",
          render: (h, params) => {
            return h("div", [
              h("i-switch", {
                props: {
                  value: params.row.is_active === true // 控制开关的打开或关闭状态，官网文档属性是value
                },
                style: {
                  marginRight: "5px"
                },
                on: {
                  "on-change": () => {
                    this.onSwitch(params, "is_active");
                  }
                }
              })
            ]);
          }
        },
        {
          title: "操作",
          align: "center",
          width: 240,
          slot: "action",
          key: "action"
        }
      ],
      // 搜索数据
      searchKey: "",
      searchValue: "",
      // 分页数据
      tableData: [],
      pageTotal: 0, // 数据总数
      pageNum: 1, // 当前页码
      pageSize: 15, // 每页条数,
      edit: false,
      roles: [],
      resetPwdformList: []
    };
  },
  methods: {
    roleNameList(rolesId) {
      let ret = [];
      for (let role of this.roles) {
        if (rolesId.indexOf(role.id) !== -1) {
          ret.push(role.name);
        }
      }
      return ret;
    },
    getRoleList() {
      listRole().then(res => {
        this.roles = res.data.list;
      });
    },
    handleDelete(row) {
      this.$Modal.confirm({
        title: this.$i18n.t("Confirm delete"),
        content: this.$i18n.t("Are you sure you want to delete {msg} ?", {
          msg: row.username
        }),
        loading: true,
        onOk: () => {
          deleteUser({ obj_id: row.id })
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
    changePage(value) {
      this.pageNum = value;
      this.getUserList(
        this.pageNum,
        this.pageSize,
        this.searchKey,
        this.searchValue
      );
    },
    // 每页条数
    handlePageSize(value) {
      this.pageSize = value;
      this.getUserList(1, this.pageSize, this.searchKey, this.searchValue);
    },
    handleSearch() {
      this.pageNum = 1;
      this.getUserList(
        this.pageNum,
        this.pageSize,
        this.searchKey,
        this.searchValue
      );
    },
    // 获取用户列表
    getUserList(page, limit, key, value) {
      let params = {
        offset: (page - 1) * limit,
        limit: limit
      };
      params[key] = value;
      listUser(params).then(res => {
        this.pageTotal = res.data.total;
        this.tableData = res.data.list;
      });
    },
    handleSubmit(value) {
      this.loading = true;
      if (this.edit) {
        delete value.data.username;
        updateUser(value.data).then(() => {
          this.$Message.success(this.$i18n.t("update success"));
          this.modalVisible = false;
          this.getUserList();
        });
      } else {
        delete value.data.obj_id;
        createUser(value.data).then(() => {
          this.$Message.success(this.$i18n.t("create success"));
          this.getUserList();
          this.modalVisible = false;
        });
      }
    },
    // 弹出对话框
    editModal(row, edit) {
      this.modalVisible = true;
      this.edit = edit;
      let tempList = [];
      for (let item of this.roles) {
        tempList.push({ value: item.id, title: item.name });
      }
      this.formList = [
        {
          name: "obj_id",
          value: edit === true ? row.id : ""
        },
        {
          name: "username",
          type: "i-input",
          disabled: edit,
          value: edit === true ? row.username : "",
          label: "用户名",
          rule: [{ required: true, message: "用户名不能为空", trigger: "blur" }]
        },
        {
          name: "nick_name",
          type: "i-input",
          value: edit === true ? row.nick_name : "",
          label: "用户昵称",
          rule: [
            { required: true, message: "用户昵称不能为空", trigger: "blur" }
          ]
        },
        {
          name: "roles",
          type: "i-select",
          value: edit === true ? row.roles : "",
          label: "角色",
          multiple: true,
          children: {
            type: "i-option",
            list: tempList
          }
        }
      ];
      if (edit === false) {
        this.formList.push({
          name: "password",
          type: "i-input",
          value: "",
          label: "密码",
          rule: [{ required: true, message: "密码不能为空", trigger: "blur" }]
        });
      }
    },
    // 调用开关
    onSwitch(params, field) {
      const row = params.row;
      let data = {
        obj_id: row.id,
        is_admin: row.is_admin,
        is_active: row.is_active,
        roles: row.roles
      };
      if (field === "is_active") {
        data.is_active = !data.is_active;
      } else if (field === "is_admin") {
        data.is_admin = !data.is_admin;
      }
      updateUser(data).then(() => {
        this.$Message.success(this.$i18n.t("update success"));
      });
    },
    handleResetPWD(row) {
      this.resetPwdModal = true;
      this.resetPwdformList = [
        {
          name: "obj_id",
          value: row.id
        },
        {
          name: "password",
          type: "i-input",
          value: "",
          label: "密码",
          rule: [{ required: true, message: "密码不能为空", trigger: "blur" }]
        }
      ];
    },
    handleResetPwdSubmit(value) {
      resetPassword(value.data).then(() => {
        this.resetPwdModal = false;
        this.$Message.success(this.$i18n.t("Reset password success"));
      });
    }
  },
  mounted() {
    this.getUserList(this.pageNum, this.pageSize);
    this.getRoleList();
  }
};
</script>

<style lang="less" scoped>
.search-con {
  padding: 10px 0;
  .search {
    &-col {
      display: inline-block;
      width: 400px;
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
