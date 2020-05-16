<template>
  <div>
    <el-row style="margin-bottom: 15px" type="flex">
        <el-dropdown trigger="click">
          <el-button plain round type="primary" size="small">
            <i class="el-icon-plus el-icon--left"></i>New Tracker
          </el-button>
          <el-dropdown-menu>
            <el-dropdown-item @click.native="dialogTrackerVisible = true">
              <router-link to="/settings?tracker=jira" tag="span">Jira</router-link>
            </el-dropdown-item>
            <el-dropdown-item disabled>
              Zentao
            </el-dropdown-item>
            <el-dropdown-item disabled>
              Bugzilla
            </el-dropdown-item>
              <el-dropdown-item @click.native="dialogTrackerVisible = true">
                <router-link to="/settings?tracker=testlink" tag="span">TestLink</router-link>
              </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
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
        <el-table-column prop="tracker" label="Tracker" width="200"></el-table-column>
        <el-table-column prop="type" label="Type" width="100"></el-table-column>
        <el-table-column prop="url" label="URL" width="300"></el-table-column>
        <el-table-column prop="account" label="Account" width="200"></el-table-column>
        <el-table-column prop="status" label="Status" width=""></el-table-column>
        <el-table-column prop="action" label="Action" width="150"></el-table-column>
      </el-table>
    </el-row>
    <el-dialog
      title="Tracker"
      :visible.sync="dialogTrackerVisible"
      width="30%">
      <InfoTracker/>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogTrackerVisible = false" size="small">Confirm</el-button>
        <el-button @click="dialogTrackerVisible = false" size="small">Cancel</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import InfoTracker from '@/components/InfoTracker.vue'
export default {
  data () {
    return {
      tableData: [
      ],
      loading: false,
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
