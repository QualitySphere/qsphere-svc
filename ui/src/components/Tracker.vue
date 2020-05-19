<template>
  <div>
    <el-row style="margin-bottom: 15px" type="flex">
      <el-button plain round type="primary" size="small" @click="dialogTrackerVisible = true">
        <i class="el-icon-plus el-icon--left"></i>New Tracker
      </el-button>
      <el-tooltip placement="bottom-start">
        <div slot="content" v-html="content"></div>
        <i class="el-icon-question el-icon--right"></i>
      </el-tooltip>
    </el-row>
    <el-row>
      <el-table
        v-loading="trackerTableLoading"
        :data="trackerTableData"
        :border="true"
        style="width: 100%;">
        <!-- <el-table-column prop="tracker" label="Tracker" width="200"></el-table-column> -->
        <!-- <el-table-column prop="type" label="Type" width="100"></el-table-column> -->
        <!-- <el-table-column prop="url" label="URL" width="300"></el-table-column> -->
        <!-- <el-table-column prop="account" label="Account" width="200"></el-table-column> -->
        <!-- <el-table-column prop="status" label="Status" width=""></el-table-column> -->
        <!-- <el-table-column prop="action" label="Action" width="150"></el-table-column> -->
        <el-table-column prop="connection_name" label="Tracker" width="200"></el-table-column>
        <el-table-column prop="issue_server.type" label="Type" width="100"></el-table-column>
        <el-table-column prop="issue_server.host" label="URL" width="200"></el-table-column>
        <el-table-column prop="issue_server.account" label="Account" width="200"></el-table-column>
        <el-table-column prop="active" label="Status" width=""></el-table-column>
        <el-table-column prop="action" label="Action" width="150"></el-table-column>
      </el-table>
    </el-row>
    <el-dialog
      title="Tracker"
      :visible.sync="dialogTrackerVisible"
      width="30%">
      <InfoTracker/>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogTrackerVisible = false" size="small">Save</el-button>
        <el-button @click="dialogTrackerVisible = false" size="small">Cancel</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import InfoTracker from '@/components/InfoTracker.vue'
// import trackerSvc from '@/services/trackerSvc'
export default {
  props: {
    trackerTableData: {
      type: Array
    },
    trackerTableLoading: {
      type: Boolean
    }
  },
  data () {
    return {
      dialogTrackerVisible: false,
      content: `
        <h3>Tracker<h3>
        This is Qsphere tracker help document<br/>
        Only for you<br/>
      `
    }
  },
  components: {
    InfoTracker
  }
}
</script>
