<template>
  <div>
    <el-row style="margin-bottom: 15px" type="flex">
      <el-button plain round type="primary" size="small" @click="initSprint(); dialogSprintVisible = true">
        <i class="el-icon-plus el-icon--left"></i>New Sprint
      </el-button>
      <el-tooltip placement="bottom-start">
        <div slot="content" v-html="content"></div>
        <i class="el-icon-question el-icon--right"></i>
      </el-tooltip>
    </el-row>
    <el-row>
      <el-table
        v-loading="sprintTableLoading"
        :data="sprintTableData"
        :border="true"
        style="width: 100%;">
        <el-table-column prop="name" label="Sprint" width="200"></el-table-column>
        <el-table-column prop="project_name" label="Project" width=""></el-table-column>
        <el-table-column
          label="Sync"
          width="100">
          <template slot-scope="scope">
            <el-button
              @click="syncSprintIssue(scope.row.id)"
              size="mini"
              icon="el-icon-refresh"
              circle>
            </el-button>
          </template>
        </el-table-column>
        <el-table-column
          label="Status"
          width="100">
          <template slot-scope="scope">
            <el-tooltip :content="'Status is ' + scope.row.status">
              <el-switch
                v-model="scope.row.status"
                @change="activeSprint(scope.row.id, scope.row.status)"
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
              @click="editSprint(scope.row.id); dialogSprintVisible = true"
              size="mini"
              type="primary"
              icon="el-icon-edit"
              circle>
            </el-button>
            <el-button
              @click="deleteSprint(scope.row.id)"
              size="mini"
              type="danger"
              icon="el-icon-delete"
              circle>
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-row>
    <el-dialog title="Sprint" :visible.sync="dialogSprintVisible" width="30%">
      <el-form
        :label-position="labelPosition"
        :border="true"
        :model="sprintData"
        label-width="120px"
        style="width: 100%;">
        <el-form-item label="Sprint Name">
          <el-input
            v-model="sprintData.name"
            placeholder="Input Sprint Name">
          </el-input>
        </el-form-item>
        <el-form-item label="Project">
          <el-select
            v-model="sprintData.project_id"
            filterable
            clearable
            @focus="listProject()"
            placeholder="Select Project"
            style="width: 100%;">
            <el-option
              v-for="item in selection.projects"
              :key="item.name"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Version">
          <el-select
            v-model="sprintData.version"
            filterable
            clearable
            allow-create
            default-first-option
            placeholder="Sprint Version Tag"
            style="width: 100%;">
            <el-option
              v-for="item in sprintData.version"
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
            filterable
            clearable
            allow-create
            default-first-option
            placeholder="Define Requirements Tags"
            style="width: 100%;">
            <el-option
              v-for="item in sprintData.requirements"
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
            filterable
            clearable
            allow-create
            default-first-option
            @focus="listRC()"
            placeholder="Define RC Tags"
            style="width: 100%;">
            <el-option
              v-for="item in selection.rcs"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <el-divider>Issue</el-divider>
        <el-form-item label="Type">
          <el-select
            v-model="sprintData.issue.types"
            multiple
            clearable
            filterable
            allow-create
            default-first-option
            @focus="listIssueType()"
            placeholder="Select Issue Type"
            style="width: 100%;">
            <el-option
              v-for="item in selection.issue_types"
              :key="item.key"
              :label="item.value"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Found Since">
          <el-select
            v-model="sprintData.issue.found_since"
            multiple
            clearable
            filterable
            allow-create
            default-first-option
            @focus="listIssueFoundSince()"
            placeholder="Define Tags For Found Since"
            style="width: 100%;">
            <el-option
              v-for="item in selection.issue_found_since"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Category">
          <el-select
            v-model="sprintData.issue.categories"
            multiple
            clearable
            filterable
            allow-create
            default-first-option
            @focus="listIssueCategories()"
            placeholder="Define Issue Category Tags"
            style="width: 100%;">
            <el-option
              v-for="item in selection.issue_categories"
              :key="item"
              :label="item"
              :value="item">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Fixing">
          <el-select
            v-model="sprintData.issue.statuses.fixing"
            multiple
            filterable
            clearable
            allow-create
            default-first-option
            @focus="listIssueStatus()"
            placeholder="Define Fixing Tags"
            style="width: 100%;">
            <el-option
              v-for="item in selection.issue_statuses"
              :key="item.key"
              :label="item.value"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Fixed">
          <el-select
            v-model="sprintData.issue.statuses.fixed"
            multiple
            filterable
            clearable
            allow-create
            default-first-option
            placeholder="Define Fixed Tags"
            style="width: 100%;">
            <el-option
              v-for="item in selection.issue_statuses"
              :key="item.key"
              :label="item.value"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Verified">
          <el-select
            v-model="sprintData.issue.statuses.verified"
            multiple
            filterable
            clearable
            allow-create
            default-first-option
            placeholder="Define Verified Tags"
            style="width: 100%;">
            <el-option
              v-for="item in selection.issue_statuses"
              :key="item.key"
              :label="item.value"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submit" size="small">Save</el-button>
        <el-button @click="dialogSprintVisible = false" size="small">Cancel</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import trackerSvc from '@/services/trackerSvc'
import projectSvc from '@/services/projectSvc'
import sprintSvc from '@/services/sprintSvc'
import issueSvc from '@/services/issueSvc'
export default {
  props: {
    sprintTableData: {
      type: Array
    },
    sprintTableLoading: {
      type: Boolean
    },
    listSprint: {
      type: Function
    }
  },
  data () {
    return {
      content: `
        Hello, Sprint
      `,
      dialogSprintVisible: false,
      labelPosition: 'left',
      selection: {
        projects: [],
        rcs: [],
        issue_types: [],
        issue_found_since: [],
        issue_categories: [],
        issue_statuses: []
      },
      sprintData: {
        project_id: '',
        name: '',
        version: '',
        requirements: [],
        rcs: [],
        issue: {
          types: [],
          found_since: [],
          statuses: {
            fixing: [],
            fixed: [],
            verified: []
          },
          categories: []
        },
        case: {}
      }
    }
  },
  methods: {
    listProject () {
      projectSvc.listProject()
        .then((response) => {
          console.log(response)
          this.selection.projects = response.data.detail.results
        })
        .catch((error) => {
          this.$message.error(String(error))
          this.selection.projects = []
        })
    },
    listIssueStatus () {
      projectSvc.getProject(this.sprintData.project_id)
        .then((response) => {
          console.log(response)
          trackerSvc.listTrackerIssueStatus(response.data.detail.tracker.issue.id)
            .then((response) => {
              console.log(response)
              this.selection.issue_statuses = response.data.detail.results
            })
            .catch((error) => {
              this.$message.error(String(error))
              this.selection.issue_statuses = []
            })
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    listIssueType () {
      projectSvc.getProject(this.sprintData.project_id)
        .then((response) => {
          console.log(response)
          console.log(response.data.detail.tracker.issue.id)
          trackerSvc.listTrackerIssueType(response.data.detail.tracker.issue.id)
            .then((response) => {
              this.selection.issue_types = response.data.detail.results
            })
            .catch((error) => {
              this.$message.error(String(error))
            })
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    listRC () {
      this.selection.rcs = ['RC1', 'RC2', 'RC3', 'RC4', 'RC5']
    },
    listIssueFoundSince () {
      this.selection.issue_found_since = ['RegressionImprove', 'QAMissed', 'NewFeature', 'Customer']
    },
    listIssueCategories () {
      this.selection.issue_categories = ['Regression', 'Previous', 'NewFeature', 'Others']
    },
    submit () {
      console.log(this.sprintData)
      if (this.sprintData.id) {
        sprintSvc.updateSprint(this.sprintData)
          .then((response) => {
            console.log(response)
            this.$message.success('Success')
            this.dialogSprintVisible = false
            this.listSprint()
          })
          .catch((error) => {
            this.$message.error(String(error))
          })
      } else {
        sprintSvc.addSprint(this.sprintData)
          .then((response) => {
            console.log(response)
            this.$message.success('Success')
            this.dialogSprintVisible = false
            this.listSprint()
          })
          .catch((error) => {
            this.$message.error(String(error))
          })
      }
    },
    activeSprint (sprintId, sprintStatus) {
      console.log('Set sprint ' + sprintId + ' status as ' + sprintStatus)
      sprintSvc.activeSprint(sprintId, sprintStatus)
        .then((response) => {
          this.$message.success('Set status as ' + sprintStatus)
          this.listSprint()
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    deleteSprint (sprintId) {
      console.log('Delete sprint' + sprintId)
      sprintSvc.deleteSprint(sprintId)
        .then((response) => {
          this.$message.success('Deleted')
          this.listSprint()
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    editSprint (sprintId) {
      this.listProject()
      console.log('Edit sprint: ' + sprintId)
      sprintSvc.getSprint(sprintId)
        .then((response) => {
          console.log(response.data.detail)
          this.sprintData.id = response.data.detail.id
          this.sprintData.name = response.data.detail.name
          this.sprintData.project_id = response.data.detail.project_id
          this.sprintData.version = response.data.detail.version
          this.sprintData.requirements = response.data.detail.requirements
          this.sprintData.rcs = response.data.detail.rcs
          this.sprintData.issue = response.data.detail.issue
          this.sprintData.case = response.data.detail.case
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    initSprint () {
      this.sprintData.id = ''
      this.sprintData.name = ''
      this.sprintData.project_id = ''
      this.sprintData.version = ''
      this.sprintData.requirements = []
      this.sprintData.rcs = []
      this.sprintData.issue = {
        types: [],
        found_since: [],
        statuses: {
          fixing: [],
          fixed: [],
          verified: []
        },
        categories: []
      }
      this.sprintData.case = {}
    },
    syncSprintIssue (sprintId) {
      console.log('Sync issue status of sprint ' + sprintId)
      this.$message.success('Start to sync')
      issueSvc.syncSprintIssue(sprintId)
        .then((response) => {
          console.log(response)
          this.$message.success('Complete to sync')
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    }
  }
}
</script>
