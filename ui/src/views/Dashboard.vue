<template>
  <div style="width: 100%; height: 100%;">
    <el-row type="flex" style="height: 5%;">
    <el-form
      :inline="true"
      size="small"
      label-position="left">
      <el-form-item
        label="Tracker">
        <el-select
          @focus="listTracker"
          v-model="tracker.id"
          placeholder="Select Tracker">
          <el-option
            v-for="item in trackers"
            :key="item.id"
            :label="item.name"
            :value="item.name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        v-if="$route.path == '/project' || $route.path == '/sprint'"
        label="Project"
        style="margin-left: 20px;">
        <el-select
          @focus="listProject"
          v-model="project.name"
          @change="updateUrlForProject"
          placeholder="Select Project">
          <el-option
            v-for="item in projects"
            :key="item.id"
            :label="item.name"
            :value="item.name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        v-if="$route.path == '/sprint'"
        label="Sprint"
        style="margin-left: 20px;">
        <el-select
          @focus="listSprint"
          v-model="sprint.name"
          @change="updateUrlForSprint"
          placeholder="Select Sprint">
          <el-option
            v-for="item in sprints"
            :key="item.id"
            :label="item.name"
            :value="item.name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        style="align: right;">
        <el-link
          icon="el-icon-full-screen"
          :underline="false"
          style="font-size: 1.25em;"
          @click="fullScreen">
        </el-link>
      </el-form-item>
    </el-form>
    </el-row>
    <iframe
      frameborder="0"
      sandbox="allow-scripts allow-same-origin"
      :src="url"
      style="width: 100%; height: 95%;">
    </iframe>
  </div>
</template>

<script>
import trackerSvc from '@/services/trackerSvc'
import projectSvc from '@/services/projectSvc'
import sprintSvc from '@/services/sprintSvc'
export default {
  data () {
    return {
      baseUrl: '/dashboard/d/qap/quality-assurance-platform?orgId=1&kiosk&refresh=1m',
      url: '/dashboard/d/qap/quality-assurance-platform?orgId=1&theme=light&kiosk&refresh=1m',
      theme: 'light',
      trackers: [],
      tracker: {
        id: '',
        name: ''
      },
      projects: [],
      project: {
        id: '',
        name: ''
      },
      sprints: [],
      sprint: {
        id: '',
        name: ''
      },
      startDate: '2020-04-30',
      endDate: '2020-05-13'
    }
  },
  methods: {
    updateUrlForProject () {
      this.sprints.sprint_name = ''
      this.url = this.baseUrl + '&theme=' + this.theme + '&var-PROJECT=' + this.projects.project_name + '&var-START_DATE=' + this.startDate + '&var-END_DATE=' + this.endDate
    },
    updateUrlForSprint () {
      this.url = this.baseUrl + '&theme=' + this.theme + '&var-PROJECT=' + this.projects.project_name + '&var-SPRINT=' + this.sprints.sprint_name + '&var-START_DATE=' + this.startDate + '&var-END_DATE=' + this.endDate
    },
    listTracker () {
      trackerSvc.listTracker()
        .then((response) => {
          console.log(response)
          this.trackers = response.data.detail.results
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    listProject () {
      projectSvc.listProject()
        .then((response) => {
          console.log(response)
          this.projects = response.data.detail.results
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    listSprint () {
      sprintSvc.listSprint()
        .then((response) => {
          console.log(response)
          this.sprints = response.data.detail.results
        })
        .catch((error) => {
          this.$message.error(String(error))
        })
    },
    fullScreen () {
      var fullScreenUrl = this.url
      window.open(fullScreenUrl.replace(/theme=light/, 'theme=dark'))
    }
  }
}
</script>
