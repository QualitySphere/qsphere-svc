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
        v-loading="loading"
        :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
        :border="true"
        style="width: 100%;">
        <el-table-column prop="project" label="Project" width="200"></el-table-column>
        <el-table-column prop="tracker" label="Tracker" width="200"></el-table-column>
        <el-table-column prop="status" label="Status" width=""></el-table-column>
        <el-table-column prop="action" label="Action" width="150"></el-table-column>
      </el-table>
    </el-row>
    <el-dialog
      title="Project"
      :visible.sync="dialogProjectVisible"
      width="30%">
      <InfoProject/>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogProjectVisible = false" size="small">Cancel</el-button>
        <el-button type="primary" @click="dialogProjectVisible = false" size="small">Confirm</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import InfoProject from '@/components/InfoProject.vue'
export default {
  data () {
    return {
      tableData: [
      ],
      loading: false,
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
