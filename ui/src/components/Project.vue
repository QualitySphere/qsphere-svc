<template>
  <div>
    <el-row style="margin-bottom: 15px" type="flex">
        <el-button plain round type="primary" size="small" @click="dialogProjectVisible = true">
          <i class="el-icon-plus el-icon--left"></i>New Project
        </el-button>
        <el-tooltip placement="bottom-start">
          <div slot="content" v-html="content"></div>
          <i class="el-icon-question el-icon--right"></i>
        </el-tooltip>
    </el-row>
    <el-row>
      <el-table
        v-loading="projectTableLoading"
        :data="projectTableData"
        :border="true"
        style="width: 100%;">
        <el-table-column prop="project_name" label="Project" width="200"></el-table-column>
        <el-table-column prop="connection_id" label="Tracker" width="200"></el-table-column>
        <el-table-column prop="active" label="Status" width=""></el-table-column>
        <el-table-column prop="action" label="Action" width="150"></el-table-column>
      </el-table>
    </el-row>
    <el-dialog
      title="Project"
      :visible.sync="dialogProjectVisible"
      width="30%">
      <InfoProject/>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogProjectVisible = false" size="small">Save</el-button>
        <el-button @click="dialogProjectVisible = false" size="small">Cancel</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import InfoProject from '@/components/InfoProject.vue'
// import projectSvc from '@/services/projectSvc'
export default {
  props: {
    projectTableData: {
      type: Array
    },
    projectTableLoading: {
      type: Boolean
    }
  },
  data () {
    return {
      dialogProjectVisible: false,
      content: `
      Hello, Project
      `
    }
  },
  components: {
    InfoProject
  }
}
</script>
