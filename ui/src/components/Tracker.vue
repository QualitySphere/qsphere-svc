<template>
  <div>
    <el-row style="margin-bottom: 15px" type="flex">
      <el-button plain round type="primary" size="small" @click="initTrackerData(); dialogTrackerVisible = true">
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
        <el-table-column
          prop="name"
          label="Tracker" width="200">
          <template slot-scope="scope">
            <span>{{ scope.row.name }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="type" label="Type" width="100"></el-table-column>
        <el-table-column prop="info.host" label="Host" width=""></el-table-column>
        <el-table-column prop="info.account" label="Account" width="200"></el-table-column>
        <el-table-column
          label="Status"
          width="100">
          <template slot-scope="scope">
            <el-tooltip :content="'Status is ' + scope.row.status">
              <el-switch
                v-model="scope.row.status"
                @change="activeTracker(scope.row.id, scope.row.status)"
                active-value='active'
                inactive-value='disable'>
              </el-switch>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column
          label="Action"
          width="150">
          <template slot-scope="scope">
            <el-button
              @click="editTracker(scope.row.id); dialogTrackerVisible = true"
              size="mini"
              type="primary"
              icon="el-icon-edit"
              circle>
            </el-button>
            <el-button
              @click="deleteTracker(scope.row.id)"
              size="mini"
              type="danger"
              icon="el-icon-delete"
              circle>
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
    <el-dialog
      title="Tracker"
      :visible.sync="dialogTrackerVisible"
      width="30%">
      <el-form
        :label-position="labelPosition"
        :border="true"
        :model="trackerData"
        label-width="120px"
        style="width: 100%;">
        <el-form-item label="Tracker Name">
          <el-input v-model="trackerData.name" placeholder="Provide Tracker Name"></el-input>
        </el-form-item>
        <el-form-item label="Tracker Type">
          <el-select
            v-model="trackerData.type"
            placeholder="Select Tracker Type"
            style="width: 100%;">
            <el-option
              v-for="item in trackerData.types"
              :key="item.type"
              :label="item.label"
              :value="item.type">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type === 'jira'"
          label="Jira Server">
          <el-input v-model="trackerData.jira.host"></el-input>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type === 'jira'"
          label="Jira Account">
          <el-input v-model="trackerData.jira.account"></el-input>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type === 'jira'"
          label="Jira Password">
          <el-input v-model="trackerData.jira.password" show-password></el-input>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type === 'testlink'"
          label="TestLink Server">
          <el-input v-model="trackerData.testlink.host"></el-input>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type === 'testlink'"
          label="TestLink Account">
          <el-input v-model="trackerData.testlink.account"></el-input>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type === 'testlink'"
          label="TestLink DevKey">
          <el-input v-model="trackerData.testlink.devkey"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submit" size="small">Save</el-button>
        <el-button @click="dialogTrackerVisible = false" size="small">Cancel</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import trackerSvc from '@/services/trackerSvc'
export default {
  props: {
    trackerTableData: {
      type: Array
    },
    trackerTableLoading: {
      type: Boolean
    },
    listTracker: {
      type: Function
    }
  },
  data () {
    return {
      dialogTrackerVisible: false,
      content: `
        <h3>Tracker<h3>
        This is Qsphere tracker help document<br/>
        Only for you<br/>
      `,
      labelPosition: 'left',
      trackerData: {
        id: '',
        name: '',
        types: [{
          type: 'jira',
          label: 'Jira'
        }],
        jira: {
          host: '',
          account: '',
          password: ''
        },
        testlink: {
          host: '',
          account: '',
          devkey: ''
        },
        status: ''
      }
    }
  },
  methods: {
    initTrackerData () {
      this.trackerData.id = ''
      this.trackerData.name = ''
      this.trackerData.status = ''
      this.trackerData.jira.host = ''
      this.trackerData.jira.account = ''
      this.trackerData.jira.password = ''
      this.trackerData.testlink.host = ''
      this.trackerData.testlink.account = ''
      this.trackerData.testlink.devkey = ''
    },
    submit () {
      console.log(this.trackerData)
      if (this.trackerData.type === 'jira') {
        var _data = {
          id: this.trackerData.id,
          name: this.trackerData.name,
          type: this.trackerData.type,
          info: {
            host: this.trackerData.jira.host,
            account: this.trackerData.jira.account
          },
          secret: this.trackerData.jira.password,
          status: this.trackerData.status
        }
      }
      if (this.trackerData.id) {
        trackerSvc.updateTracker(_data)
          .then((response) => {
            this.$message.success('Success')
            this.dialogTrackerVisible = false
            this.listTracker()
          })
          .catch((error) => {
            this.$message.error(String(error))
          })
      } else {
        trackerSvc.addTracker(_data)
          .then((response) => {
            this.$message.success('Success')
            this.dialogTrackerVisible = false
            this.listTracker()
          })
          .catch((error) => {
            this.$message.error(String(error))
          })
      }
    },
    editTracker (trackerId) {
      console.log('Edit tracker: ' + trackerId)
      trackerSvc.getTracker(trackerId)
        .then((response) => {
          console.log(response.data.detail)
          this.trackerData.id = response.data.detail.id
          this.trackerData.name = response.data.detail.name
          this.trackerData.type = response.data.detail.type
          if (this.trackerData.type === 'jira') {
            this.trackerData.jira.host = response.data.detail.info.host
            this.trackerData.jira.account = response.data.detail.info.account
            this.trackerData.jira.password = ''
          }
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    deleteTracker (trackerId) {
      console.log('Delete tracker: ' + trackerId)
      trackerSvc.deleteTracker(trackerId)
        .then((response) => {
          this.$message.success('Deleted')
          this.listTracker()
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    activeTracker (trackerId, trackerStatus) {
      console.log('Set tracker ' + trackerId + ' status as ' + trackerStatus)
      trackerSvc.activeTracker(trackerId, trackerStatus)
        .then((response) => {
          this.$message.success('Set status as ' + trackerStatus)
          this.listTracker()
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    }
  }
}
</script>
