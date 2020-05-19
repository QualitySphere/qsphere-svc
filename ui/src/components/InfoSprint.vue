<template>
  <el-form
    :label-position="labelPosition"
    :border="true"
    :model="sprintData"
    label-width="120px"
    style="width: 100%;">
    <el-form-item label="Tracker">
      <el-input v-model="sprintData.name" placeholder="Provide Sprint Name"></el-input>
    </el-form-item>
    <el-form-item label="Type">
      <el-select
        v-model="trackerData.project"
        placeholder="Select Project"
        style="width: 100%;">
        <el-option
          v-for="item in trackerData.projects"
          :key="item.name"
          :label="item.name"
          :value="item.id">
        </el-option>
      </el-select>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data () {
    return {
      labelPosition: 'left',
      sprintData: {
        name: '',
        projects: this.listProject(),
        sprints: this.listSprint(),
        issueTypes: [],
        requirements: [],
        rcs: [],
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
  },
  methods: {
    listProject () {
      return []
    },
    listSprint () {
      return []
    }
  }
}
</script>
