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
          v-model="trackers.connection_name"
          placeholder="Select Tracker">
          <el-option
            v-for="item in trackers"
            :key="item.connection_id"
            :label="item.connection_name"
            :value="item.connection_name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        v-if="$route.path == '/project' || $route.path == '/sprint'"
        label="Project"
        style="margin-left: 20px;">
        <el-select
          @focus="listProject"
          v-model="projects.project_name"
          @change="updateUrlForProject"
          placeholder="Select Project">
          <el-option
            v-for="item in projects"
            :key="item.project_id"
            :label="item.project_name"
            :value="item.project_name">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        v-if="$route.path == '/sprint'"
        label="Sprint"
        style="margin-left: 20px;">
        <el-select
          @focus="listSprint"
          v-model="sprints.sprint_name"
          @change="updateUrlForSprint"
          placeholder="Select Sprint">
          <el-option
            v-for="item in sprints"
            :key="item.sprint_id"
            :label="item.sprint_name"
            :value="item.sprint_name">
          </el-option>
        </el-select>
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
import axios from 'axios'
export default {
  data () {
    return {
      baseUrl: '/dashboard/d/qap/quality-assurance-platform?orgId=1&theme=light&kiosk&refresh=1m',
      url: '/dashboard/d/qap/quality-assurance-platform?orgId=1&theme=light&kiosk&refresh=1m',
      trackers: [],
      projects: [],
      sprints: [],
      startDate: '2020-04-30',
      endDate: '2020-05-13'
    }
  },
  methods: {
    updateUrlForProject () {
      this.sprints.sprint_name = ''
      this.url = this.baseUrl + '&var-PROJECT=' + this.projects.project_name + '&var-START_DATE=' + this.startDate + '&var-END_DATE=' + this.endDate
    },
    updateUrlForSprint () {
      this.url = this.baseUrl + '&var-PROJECT=' + this.projects.project_name + '&var-SPRINT=' + this.sprints.sprint_name + '&var-START_DATE=' + this.startDate + '&var-END_DATE=' + this.endDate
    },
    listTracker () {
      axios.get('/api/connection')
        .then((response) => {
          console.log(response)
          this.trackers = response.data.detail.results
        })
        .catch((error) => {
          console.log(error)
        })
    },
    listProject () {
      axios.get('/api/project')
        .then((response) => {
          console.log(response)
          this.projects = response.data.detail.results
        })
        .catch((error) => {
          console.log(error)
        })
    },
    listSprint () {
      axios.get('/api/sprint')
        .then((response) => {
          console.log(response)
          this.sprints = response.data.detail.results
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>
