<template>
  <div>
    <el-row style="margin-bottom: 15px" type="flex">
      <el-button plain round type="primary" size="small" @click="dialogSprintVisible = true">
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
        <el-table-column prop="project_name" label="Project" width="200"></el-table-column>
        <el-table-column prop="status" label="Status" width></el-table-column>
        <el-table-column prop="action" label="Action" width="150"></el-table-column>
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
              v-for="item in projects"
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
            placeholder="Define RC Tags"
            style="width: 100%;">
            <el-option
              v-for="item in sprintData.rcs"
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
            placeholder="Define Tags For Issue Type"
            style="width: 100%;">
            <el-option
              v-for="item in sprintData.issue.types"
              :key="item"
              :label="item"
              :value="item">
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
            placeholder="Define Tags For Found Since"
            style="width: 100%;">
            <el-option
              v-for="item in sprintData.issue.found_since"
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
            placeholder="Define Issue Category Tags"
            style="width: 100%;">
            <el-option
              v-for="item in sprintData.issue.categories"
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
            placeholder="Define Fixing Tags"
            style="width: 100%;">
            <el-option
              v-for="item in sprintData.issue.statuses.fixing"
              :key="item"
              :label="item"
              :value="item">
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
              v-for="item in sprintData.issue.statuses.fixed"
              :key="item"
              :label="item"
              :value="item">
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
              v-for="item in sprintData.issue.statuses.verified"
              :key="item"
              :label="item"
              :value="item">
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
import projectSvc from '@/services/projectSvc'
import sprintSvc from '@/services/sprintSvc'
export default {
  props: {
    sprintTableData: {
      type: Array
    },
    sprintTableLoading: {
      type: Boolean
    }
  },
  data () {
    return {
      content: `
        Hello, Sprint
      `,
      dialogSprintVisible: false,
      labelPosition: 'left',
      projects: [],
      sprintData: {
        project_id: '',
        name: '',
        version: '',
        requirements: [],
        rcs: [],
        issue: {
          types: [],
          found_since: ['RegressionImprove', 'QAMissed', 'NewFeature', 'Customer'],
          statuses: {
            fixing: [],
            fixed: [],
            verified: []
          },
          categories: ['regression', 'previous', 'newfeature', 'others']
        },
        case: {}
      }
    }
  },
  methods: {
    listProject () {
      this.tracker_id = ''
      projectSvc.listProject()
        .then((response) => {
          this.projects = response.data.detail.results
          this.tracker_id = ''
        })
      return []
    },
    listRC () {
      return ['RC1', 'RC2', 'RC3', 'RC4', 'RC5']
    },
    submit () {
      console.log(this.sprintData)
      sprintSvc.addSprint(this.sprintData)
        .then((response) => {
          this.$message.success('Success')
          this.dialogSprintVisible = false
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    }
  }
}
</script>
