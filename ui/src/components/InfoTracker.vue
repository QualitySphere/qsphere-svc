<template>
  <el-form
    :label-position="labelPosition"
    :border="true"
    :model="trackerData"
    label-width="120px"
    style="width: 100%;">
    <el-form-item label="Tracker">
      <el-input v-model="trackerData.name" placeholder="Provide Tracker Name"></el-input>
    </el-form-item>
    <el-form-item label="Type">
      <el-select
        v-model="trackerData.type"
        placeholder="Select Tracker Type"
        style="width: 100%;">
        <el-option
          v-for="item in trackerData.types"
          :key="item.type"
          :label="item.label"
          :value="item.type">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item
      v-if="trackerData.type == 'jira'"
      label="Jira Server">
      <el-input v-model="trackerData.jira.server"></el-input>
    </el-form-item>
    <el-form-item
      v-if="trackerData.type == 'jira'"
      label="Jira User">
      <el-input v-model="trackerData.jira.user"></el-input>
    </el-form-item>
    <el-form-item
      v-if="trackerData.type == 'jira'"
      label="Jira Password">
      <el-input v-model="trackerData.jira.password" show-password></el-input>
    </el-form-item>
    <el-form-item
      v-if="trackerData.type == 'testlink'"
      label="TestLink Server">
      <el-input v-model="trackerData.testlink.server"></el-input>
    </el-form-item>
    <el-form-item
      v-if="trackerData.type == 'testlink'"
      label="TestLink User">
      <el-input v-model="trackerData.testlink.user"></el-input>
    </el-form-item>
    <el-form-item
      v-if="trackerData.type == 'testlink'"
      label="TestLink DevKey">
      <el-input v-model="trackerData.testlink.devkey"></el-input>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data () {
    return {
      labelPosition: 'left',
      trackerData: {
        name: '',
        types: [{
          type: 'jira',
          label: 'Jira'
        }, {
          type: 'testlink',
          label: 'TestLink'
        }],
        jira: {
          server: '',
          user: '',
          password: ''
        },
        testlink: {
          server: '',
          user: '',
          devkey: ''
        }
      }
    }
  }
}
</script>
