<template>
  <Form ref="form" :model="valueList" :rules="rules" :label-width="110">
    <FormItem
      v-for="(item, index) in list.filter(x => x.type !== '')"
      :label="item.label"
      label-position="left"
      :prop="item.name"
      :error="errorStore[item.name]"
      :key="`${_uid}_${index}`"
      @click.native="handleFocus(item.name)"
    >
      <Input
        v-if="item.type === 'i-input'"
        v-model="valueList[item.name]"
        :placeholder="item.placeholder ? item.placeholder : ''"
      ></Input>
      <Input
        v-if="item.type === 'textarea'"
        type="textarea"
        :placeholder="item.placeholder ? item.placeholder : ''"
        v-model="valueList[item.name]"
      ></Input>
      <template v-if="item.type === 'i-select'">
        <Row>
          <Col span="15" style="padding-right:10px">
            <Select
              v-model="valueList[item.name]"
              :placeholder="item.placeholder ? item.placeholder : ''"
            >
              <Option
                v-for="(item, i) in item.children"
                :value="item.value"
                :label="item.label"
                :key="`${_uid}_${i}`"
              ></Option>
            </Select>
          </Col>
          <Col span="9">
            <Button type="primary" @click="addCategory">添加类别</Button>
          </Col>
        </Row>
      </template>
      <template v-if="item.type === 'username'">
        <Row>
          <Col span="8">
            <Input
              v-model="valueList['username']"
              :placeholder="item.placeholder ? item.placeholder : ''"
            >
              <span slot="prepend">ssh</span>
            </Input>
          </Col>
          <Col span="8">
            <Input
              v-model="valueList['hostname']"
              :placeholder="list[4].placeholder ? list[4].placeholder : ''"
            >
              <span slot="prepend">@</span>
            </Input>
          </Col>

          <Col span="8">
            <Input
              v-model="valueList['port']"
              type="number"
              :placeholder="list[5].placeholder ? list[5].placeholder : ''"
            >
              <span slot="prepend">-p</span>
            </Input>
          </Col>
        </Row>
      </template>
    </FormItem>
    <span style="margin-left:80px">
      ⚠️ 首次验证时需要输入登录用户名对应的密码，但不会存储该密码。</span
    >
    <FormItem style="margin-top:20px">
      <slot name="right-btn"></slot>
      <Button @click="handleSubmit" type="primary" :loading="loading"
        >提交</Button
      >
      <Button @click="handleReset" style="margin-left: 8px">重置</Button>
      <slot name="left-btn"></slot>
    </FormItem>
  </Form>
</template>

<script>
import clonedeep from "clonedeep";

export default {
  props: {
    list: {
      type: Array,
      default: () => []
    }
  },
  watch: {
    list() {
      this.setInitValue();
    }
  },
  data() {
    return {
      loading: false,
      rules: {},
      valueList: {},
      errorStore: {},
      initValueList: {},
      tempCategory: "",
      form: { temp: "" }
    };
  },
  methods: {
    setInitValue() {
      let rules = {};
      let valueList = {};
      let errorStore = {};
      let initValueList = {};

      this.list.forEach(item => {
        rules[item.name] = item.rule;
        valueList[item.name] = item.value;
        initValueList[item.name] = item.value;
        errorStore[item.name] = "";
      });
      this.rules = rules;
      this.valueList = valueList;
      this.errorStore = errorStore;
      this.initValueList = initValueList;
    },
    handleSubmit() {
      this.$refs.form.validate(valid => {
        if (valid) {
          this.$emit("on-submit-success", {
            data: this.valueList
          });
          // 按钮loading
          this.loading = true;
          setTimeout(() => {
            this.loading = false;
          }, 1000);
        }
      });
    },
    handleReset() {
      this.valueList = clonedeep(this.initValueList);
    },
    handleFocus(name) {
      this.errorStore[name] = "";
    },
    addCategory() {
      this.$Modal.confirm({
        render: h => {
          return h(
            "Form",
            {
              props: {
                labelPosition: "left",
                model: this.form,
                labelWidth: 80
              }
            },
            [
              h(
                "FormItem",
                {
                  props: {
                    label: "主机类别",
                    prop: "temp",
                    rules: [
                      {
                        required: true,
                        message: "主机类别不能为空",
                        trigger: "blur"
                      }
                    ]
                  }
                },
                [
                  h("Input", {
                    props: {
                      value: "",
                      model: this.form["temp"]
                    },
                    on: {
                      input: val => {
                        this.form["temp"] = val;
                      }
                    }
                  })
                ]
              )
            ]
          );
        },
        title: "添加主机类别",

        onOk: () => {
          const val = this.form["temp"];
          this.valueList["category"] = val;
          this.list[1].children.push({ label: val, value: val });
        }
      });
    }
  }
};
</script>

<style></style>
