import axios from 'axios'

export default {

  listProject () {
    return axios.get('/api/project')
  },

  addProject (projectData) {
    var _data = {
      name: projectData.name,
      tracker: {
        issue: {
          id: projectData.tracker.issue.id,
          name: projectData.tracker.issue.name
        },
        case: {
          id: projectData.tracker.case.id,
          name: projectData.tracker.case.name
        }
      },
      project: {
        issue: {
          key: projectData.project.issue.key
        },
        case: {
          key: projectData.project.case.key
        }
      }
    }
    return axios.post('/api/project', _data)
  },

  updateProject (projectData) {
    var _data = {
      name: projectData.name,
      tracker: {
        issue: {
          id: projectData.tracker.issue.id
        },
        case: {
          id: projectData.tracker.case.id
        }
      },
      project: {
        issue: {
          key: projectData.project.issue.key,
          value: projectData.project.issue.value
        },
        case: {
          key: projectData.project.case.key,
          value: projectData.project.case.value
        }
      }
    }
    return axios.put('/api/project/' + projectData.id, _data)
  },

  getProject (projectId) {
    return axios.get('/api/project/' + projectId)
  },

  deleteProject (projectId) {
    return axios.delete('/api/project/' + projectId)
  },

  activeProject (projectId, projectStatus) {
    if (projectStatus === 'active') {
      return axios.put('/api/project/' + projectId + '/active')
    } else {
      return axios.put('/api/project/' + projectId + '/disable')
    }
  }
}
