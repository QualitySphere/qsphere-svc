import axios from 'axios'

export default {

  listSprint () {
    return axios.get('/api/sprint')
  },

  getSprint (sprintId) {
    return axios.get('/api/sprint/' + sprintId)
  },

  deleteSprint (sprintId) {
    return axios.delete('/api/sprint/' + sprintId)
  },

  activeSprint (sprintId, sprintStatus) {
    if (sprintStatus === 'active') {
      return axios.put('/api/sprint/' + sprintId + '/active')
    } else {
      return axios.put('/api/sprint/' + sprintId + '/disable')
    }
  },

  addSprint (sprintData) {
    var _data = {
      project_id: sprintData.project_id,
      name: sprintData.name,
      version: sprintData.version,
      requirements: sprintData.requirements,
      rcs: sprintData.rcs,
      issue: {
        types: sprintData.issue.types,
        found_since: sprintData.issue.found_since,
        statuses: {
          fixing: sprintData.issue.statuses.fixing,
          fixed: sprintData.issue.statuses.fixed,
          verified: sprintData.issue.statuses.verified
        },
        categories: sprintData.issue.categories
      },
      case: {}
    }
    return axios.post('/api/sprint', _data)
  },

  updateSprint (sprintData) {
    var _data = {
      project_id: sprintData.project_id,
      name: sprintData.name,
      version: sprintData.version,
      requirements: sprintData.requirements,
      rcs: sprintData.rcs,
      issue: {
        types: sprintData.issue.types,
        found_since: sprintData.issue.found_since,
        statuses: {
          fixing: sprintData.issue.statuses.fixing,
          fixed: sprintData.issue.statuses.fixed,
          verified: sprintData.issue.statuses.verified
        },
        categories: sprintData.issue.categories
      },
      case: {}
    }
    return axios.put('/api/sprint/' + sprintData.id, _data)
  }
}
