<template>
  <el-form
    :label-position="labelPosition"
    :border="true"
    :model="trackerData"
    label-width="120px"
    style="width: 100%;">
    <el-form-item label="Tracker">
      <el-input v-model="trackerData.name"></el-input>
    </el-form-item>
    <el-form-item label="Type">
      <el-input v-model="this.$route.query.tracker" disabled></el-input>
    </el-form-item>
    <el-form-item label="Jira Server" v-if="this.$route.query.tracker == 'jira'">
      <el-input v-model="trackerData.jira.server"></el-input>
    </el-form-item>
    <el-form-item label="Jira User" v-if="this.$route.query.tracker == 'jira'">
      <el-input v-model="trackerData.jira.user"></el-input>
    </el-form-item>
    <el-form-item label="Jira Password" v-if="this.$route.query.tracker == 'jira'">
      <el-input v-model="trackerData.jira.password" show-password></el-input>
    </el-form-item>
    <el-form-item label="TestLink Server" v-if="this.$route.query.tracker == 'testlink'">
      <el-input v-model="trackerData.testlink.server"></el-input>
    </el-form-item>
    <el-form-item label="TestLink User" v-if="this.$route.query.tracker == 'testlink'">
      <el-input v-model="trackerData.testlink.user"></el-input>
    </el-form-item>
    <el-form-item label="TestLink DevKey" v-if="this.$route.query.tracker == 'testlink'">
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
