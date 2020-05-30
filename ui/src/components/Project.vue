<template>
  <div>
    <el-row style="margin-bottom: 15px" type="flex">
        <el-button plain round type="primary" size="small" @click="initProjectData(); dialogProjectVisible = true">
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
        <el-table-column prop="name" label="Project" width="200"></el-table-column>
        <el-table-column prop="tracker.issue.name" label="Issue Tracker" width=""></el-table-column>
        <el-table-column prop="project.issue.key" label="Issue Project" width=""></el-table-column>
        <el-table-column prop="tracker.case.name" label="Case Tracker" width=""></el-table-column>
        <el-table-column prop="project.case.key" label="Case Project" width=""></el-table-column>
        <el-table-column
          label="Status"
          width="100">
          <template slot-scope="scope">
            <el-tooltip :content="'Status is ' + scope.row.status">
              <el-switch
                v-model="scope.row.status"
                @change="activeProject(scope.row.id, scope.row.status)"
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
              @click="editProject(scope.row.id); dialogProjectVisible = true"
              size="mini"
              type="primary"
              icon="el-icon-edit"
              circle>
            </el-button>
            <el-button
              @click="deleteProject(scope.row.id)"
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
      title="Project"
      :visible.sync="dialogProjectVisible"
      width="30%">
      <el-form
        :label-position="labelPosition"
        :border="true"
        :model="projectData"
        label-width="120px"
        style="width: 100%;">
        <el-form-item label="Project Name">
          <el-input v-model="projectData.name" placeholder="Provide Project Name"></el-input>
        </el-form-item>
        <el-form-item label="Issue Tracker">
          <el-select
            v-model="projectData.tracker.issue.id"
            @focus="listIssueTracker()"
            filterable
            clearable
            placeholder="Select Tracker"
            style="width: 100%;">
            <el-option
              v-for="item in issueTrackers"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Issue Project">
          <el-select
            v-model="projectData.project.issue.key"
            @focus="listIssueTrackerProject()"
            filterable
            clearable
            placeholder="Select Project From Tracker"
            style="width: 100%;">
            <el-option
              v-for="item in issueTrackerProjects"
              :key="item.key"
              :label="item.value"
              :value="item.key">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Case Tracker">
          <el-select
            v-model="projectData.tracker.case.id"
            @focus="listCaseTracker()"
            filterable
            clearable
            placeholder="Select Tracker"
            style="width: 100%;">
            <el-option
              v-for="item in caseTrackers"
              :key="item.id"
              :label="item.name"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Case Project">
          <el-select
            v-model="projectData.project.case.key"
            @focus="listCaseTrackerProject()"
            filterable
            clearable
            placeholder="Select Project From Tracker"
            style="width: 100%;">
            <el-option
              v-for="item in caseTrackerProjects"
              :key="item.key"
              :label="item.value"
              :value="item.key">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submit" size="small">Save</el-button>
        <el-button @click="dialogProjectVisible = false" size="small">Cancel</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import trackerSvc from '@/services/trackerSvc'
import projectSvc from '@/services/projectSvc'
export default {
  props: {
    projectTableData: {
      type: Array
    },
    projectTableLoading: {
      type: Boolean
    },
    listProject: {
      type: Function
    }
  },
  data () {
    return {
      dialogProjectVisible: false,
      content: `
      Hello, Project
      `,
      labelPosition: 'left',
      issueTrackers: {},
      issueTrackerProjects: {},
      caseTrackers: {},
      caseTrackerProjects: {},
      projectData: {
        id: '',
        name: '',
        tracker: {
          issue: {
            id: ''
          },
          case: {
            id: ''
          }
        },
        project: {
          issue: {
            key: ''
          },
          case: {
            key: ''
          }
        },
        status: ''
      }
    }
  },
  methods: {
    listIssueTracker () {
      trackerSvc.listTracker()
        .then((response) => {
          this.issueTrackers = response.data.detail.results
          console.log(this.issueTrackers)
        })
    },
    listCaseTracker () {
      trackerSvc.listTracker()
        .then((response) => {
          this.caseTrackers = response.data.detail.results
          console.log(this.caseTrackers)
        })
    },
    listIssueTrackerProject () {
      trackerSvc.listTrackerProject(this.projectData.tracker.issue.id)
        .then((response) => {
          this.issueTrackerProjects = response.data.detail.results
          console.log(this.issueTrackerProjects)
        })
    },
    listCaseTrackerProject () {
      trackerSvc.listTrackerProject(this.projectData.tracker.case.id)
        .then((response) => {
          this.caseTrackerProjects = response.data.detail.results
          console.log(this.caseTrackerProjects)
        })
    },
    initProjectData () {
      this.projectData.id = ''
      this.projectData.name = ''
      this.projectData.status = ''
      this.projectData.tracker = {
        issue: {
          id: ''
        },
        case: {
          id: ''
        }
      }
      this.projectData.project = {
        issue: {
          key: ''
        },
        case: {
          key: ''
        }
      }
    },
    submit () {
      if (this.projectData.id) {
        projectSvc.updateProject(this.projectData)
          .then((reponse) => {
            this.projectData.id = reponse.data.detail.id
            this.$message.success('Success')
            this.dialogProjectVisible = false
            this.listProject()
          })
          .catch((error) => {
            this.$message.error(String(error))
          })
      } else {
        projectSvc.addProject(this.projectData)
          .then((reponse) => {
            this.projectData.id = reponse.data.detail.id
            this.$message.success('Success')
            this.dialogProjectVisible = false
            this.listProject()
          })
          .catch((error) => {
            this.$message.error(String(error))
          })
      }
    },
    editProject (projectId) {
      this.listIssueTracker()
      this.listCaseTracker()
      console.log('Edit project: ' + projectId)
      projectSvc.getProject(projectId)
        .then((response) => {
          console.log(response.data.detail)
          this.projectData.id = response.data.detail.id
          this.projectData.name = response.data.detail.name
          this.projectData.tracker = response.data.detail.tracker
          this.projectData.project = response.data.detail.project
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    deleteProject (projectId) {
      console.log('Delete project ' + projectId)
      projectSvc.deleteProject(projectId)
        .then((response) => {
          this.$message.success('Deleted')
          this.listProject()
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    activeProject (projectId, projectStatus) {
      console.log('Set project ' + projectId + ' status as ' + projectStatus)
      projectSvc.activeProject(projectId, projectStatus)
        .then((response) => {
          this.$message.success('Set status as ' + projectStatus)
          this.listProject()
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    }
  }
}
</script>
