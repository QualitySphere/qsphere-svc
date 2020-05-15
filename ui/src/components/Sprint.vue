<template>
  <div>
    <el-row style="margin-bottom: 15px">
      <el-col :span="3">
        <router-link to="sprint" append>
          <el-button plain round type="primary" size="small">
            <i class="el-icon-circle-plus el-icon--left"></i>New Sprint
          </el-button>
        </router-link>
        <el-tooltip placement="bottom-start">
          <div slot="content" v-html="content"></div>
          <i class="el-icon-question el-icon--right"></i>
        </el-tooltip>
      </el-col>
    </el-row>
    <el-row>
      <el-table
        v-loading="loading"
        :data="tableData.filter(data => !search || data.name.toLowerCase().includes(search.toLowerCase()))"
        :border="true"
        style="width: 100%;">
        <el-table-column prop="sprint" label="Sprint" width="200"></el-table-column>
        <el-table-column prop="project" label="Project" width="200"></el-table-column>
        <el-table-column prop="tracker" label="Tracker" width="200"></el-table-column>
        <el-table-column prop="status" label="Status" width=""></el-table-column>
        <el-table-column prop="action" label="Action" width="150"></el-table-column>
      </el-table>
    </el-row>
  </div>
</template>

<script>
export default {
  data () {
    return {
      tableData: [
      ],
      loading: false,
      content: `
      Hello, Sprint
      `
    }
  }
}
</script>
