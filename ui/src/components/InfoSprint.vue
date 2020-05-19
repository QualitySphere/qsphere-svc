<template>
  <el-form
    :label-position="labelPosition"
    :border="true"
    :model="sprintData"
    label-width="120px"
    style="width: 100%;">
    <el-form-item label="Sprint Name">
      <el-input v-model="sprintData.name" placeholder="Provide Sprint Name"></el-input>
    </el-form-item>
    <el-form-item label="Project">
      <el-select
        v-model="sprintData.projects"
        placeholder="Select Project"
        style="width: 100%;">
        <el-option
          v-for="item in listTrackerProject()"
          :key="item.name"
          :label="item.name"
          :value="item.id">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Sprint">
      <el-select
        v-model="sprintData.sprints"
        placeholder="Select Sprint"
        style="width: 100%;">
        <el-option
          v-for="item in listTrackerSprint()"
          :key="item.name"
          :label="item.name"
          :value="item.id">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Issue Type">
      <el-select
        v-model="sprintData.issueTypes"
        multiple
        placeholder="Select Type"
        style="width: 100%;">
        <el-option
          v-for="item in listTrackerIssueType()"
          :key="item"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Requirement">
      <el-select
        v-model="sprintData.requirements"
        multiple
        placeholder="Select Requirement Tags"
        style="width: 100%;">
        <el-option
          v-for="item in listTrackerRequirement()"
          :key="item"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="RC">
      <el-select
        v-model="sprintData.rcs"
        multiple
        placeholder="Select RC Tags"
        style="width: 100%;">
        <el-option
          v-for="item in listRC()"
          :key="item"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="To Be Fixed">
      <el-select
        v-model="sprintData.toBeFixed"
        multiple
        placeholder="Select To Be Fixed Tags"
        style="width: 100%;">
        <el-option
          v-for="item in []"
          :key="item"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Fixed">
      <el-select
        v-model="sprintData.fixed"
        multiple
        placeholder="Select Fixed Tags"
        style="width: 100%;">
        <el-option
          v-for="item in []"
          :key="item"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="To Be Verified">
      <el-select
        v-model="sprintData.toBeVerified"
        multiple
        placeholder="Select To Be Verified Tags"
        style="width: 100%;">
        <el-option
          v-for="item in []"
          :key="item"
          :label="item"
          :value="item">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="Issue Category">
      <el-select
        v-model="sprintData.categoires"
        multiple
        placeholder="Select Category Tags"
        style="width: 100%;">
        <el-option
          v-for="item in []"
          :key="item"
          :label="item"
          :value="item">
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
        projects: [],
        sprints: [],
        issueTypes: [],
        requirements: [],
        rcs: [],
        rcList: [],
        toBeFixed: [],
        fixed: [],
        toBeVerified: [],
        categoires: []
      }
    }
  },
  methods: {
    listTrackerProject () {
      return []
    },
    listTrackerSprint () {
      return []
    },
    listTrackerIssueType () {
      return []
    },
    listTrackerRequirement () {
      return []
    },
    listRC () {
      return ['RC1', 'RC2', 'RC3', 'RC4', 'RC5']
    }
  }
}
</script>
