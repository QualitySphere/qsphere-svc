<template>
  <el-form
    :label-position="labelPosition"
    :border="true"
    :model="trackerData"
    label-width="120px"
    style="width: 100%;">
    <el-form-item label="Project Name">
      <el-input v-model="projectData.name" placeholder="Provide Project Name"></el-input>
    </el-form-item>
    <el-form-item label="Issue Tracker">
      <el-select
        v-model="projectData.project"
        placeholder="Select Tracker"
        style="width: 100%;">
        <el-option
          v-for="item in projectData.projects"
          :key="item.id"
          :label="item.label"
          :value="item.type">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Issue Project">
      <el-select
        v-model="projectData.project"
        placeholder="Select Project From Tracker"
        style="width: 100%;">
        <el-option
          v-for="item in projectData.projects"
          :key="item.id"
          :label="item.label"
          :value="item.type">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Case Tracker">
      <el-select
        v-model="projectData.project"
        placeholder="Select Tracker"
        style="width: 100%;">
        <el-option
          v-for="item in projectData.projects"
          :key="item.id"
          :label="item.label"
          :value="item.type">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Case Project">
      <el-select
        v-model="projectData.project"
        placeholder="Select Project From Tracker"
        style="width: 100%;">
        <el-option
          v-for="item in projectData.projects"
          :key="item.id"
          :label="item.label"
          :value="item.type">
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
      projectData: {
        id: '',
        name: '',
        trackers: [{
          tracker: '',
          label: ''
        }],
        tracker: '',
        projects: [{
          project: '',
          label: ''
        }],
        project: ''
      }
    }
  }
}
</script>
