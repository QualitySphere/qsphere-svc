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
        <el-table-column prop="name" label="Tracker" width="200"></el-table-column>
        <el-table-column prop="type" label="Type" width="100"></el-table-column>
        <el-table-column prop="info.host" label="Host" width="300"></el-table-column>
        <el-table-column prop="info.account" label="Account" width="200"></el-table-column>
        <el-table-column prop="status" label="Status" width=""></el-table-column>
        <el-table-column prop="action" label="Action" width="150"></el-table-column>
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
          v-if="trackerData.type == 'jira'"
          label="Jira Server">
          <el-input v-model="trackerData.jira.host"></el-input>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type == 'jira'"
          label="Jira Account">
          <el-input v-model="trackerData.jira.account"></el-input>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type == 'jira'"
          label="Jira Password">
          <el-input v-model="trackerData.jira.password" show-password></el-input>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type == 'testlink'"
          label="TestLink Server">
          <el-input v-model="trackerData.testlink.host"></el-input>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type == 'testlink'"
          label="TestLink Account">
          <el-input v-model="trackerData.testlink.account"></el-input>
        </el-form-item>
        <el-form-item
          v-if="trackerData.type == 'testlink'"
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
        }
      }
    }
  },
  methods: {
    submit () {
      console.log(this.trackerData)
      if (this.trackerData.type === 'jira') {
        var _data = {
          name: this.trackerData.name,
          type: this.trackerData.type,
          info: {
            host: this.trackerData.jira.host,
            account: this.trackerData.jira.account
          },
          secret: this.trackerData.jira.password
        }
      }
      trackerSvc.addTracker(_data)
        .then((response) => {
          this.$message.success('Success')
          this.dialogTrackerVisible = false
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    }
  }
}
</script>
