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
      baseUrl: '/dashboard/d/qsphere/quality-sphere?orgId=1&kiosk&refresh=1m',
      url: '/dashboard/d/qsphere/quality-sphere?orgId=1&theme=light&kiosk&refresh=1m',
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
      startDate: '',
      endDate: ''
    }
  },
  methods: {
    updateUrlForProject () {
      this.sprint.name = ''
      this.url = this.baseUrl + '&theme=' + this.theme + '&var-PROJECT=' + this.project.name + '&from=' + this.startDate + '&to=' + this.endDate
      console.log(this.url)
    },
    updateUrlForSprint () {
      for (var s in this.sprints) {
        console.log(this.sprints[s])
        if (this.sprints[s].name === this.sprint.name) {
          this.sprint.id = this.sprints[s].id
          break
        }
      }
      console.log(this.sprint.id)
      sprintSvc.getSprint(this.sprint.id)
        .then((response) => {
          console.log(response)
          this.startDate = response.data.detail.start_time
          console.log(this.startDate)
          this.endDate = response.data.detail.end_time
          console.log(this.endDate)
          this.url = this.baseUrl + '&theme=' + this.theme + '&var-PROJECT=' + this.project.name + '&var-SPRINT=' + this.sprint.name + '&from=' + this.startDate + '&to=' + this.endDate
          console.log(this.url)
        })
        .catch((error) => {
          this.$message.error(error)
        })
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
