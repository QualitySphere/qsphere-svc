<template>
  <div>
    <el-row style="margin-bottom: 15px">
      <el-col :span="3">
        <el-dropdown trigger="click">
          <el-button plain round type="primary" size="small">
            <i class="el-icon-circle-plus el-icon--left"></i>New Tracker
          </el-button>
          <el-dropdown-menu>
            <el-dropdown-item>
              <router-link :to="{path: 'tracker', query: {type: 'jira'}}" tag="span" append>
                Jira
              </router-link>
            </el-dropdown-item>
            <el-dropdown-item disabled>
              <router-link :to="{path: 'tracker', query: {type: 'zentao'}}" tag="span" append>
                Zentao
              </router-link>
            </el-dropdown-item>
            <el-dropdown-item disabled>
              <router-link :to="{path: 'tracker', query: {type: 'testlink'}}" tag="span" append>
                TestLink
              </router-link>
            </el-dropdown-item>
            <el-dropdown-item disabled>
              <router-link :to="{path: 'tracker', query: {type: 'bugzilla'}}" tag="span" append>
                Bugzilla
              </router-link>
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
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
        <el-table-column prop="tracker" label="Tracker" width="200"></el-table-column>
        <el-table-column prop="type" label="Type" width="100"></el-table-column>
        <el-table-column prop="url" label="URL" width="300"></el-table-column>
        <el-table-column prop="account" label="Account" width="200"></el-table-column>
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
      <h3>Tracker<h3>
      This is Qsphere tracker help document<br/>
      Only for you<br/>
      `
    }
  }
}
</script>
