import axios from 'axios'

export default {

  listTracker () {
    return axios.get('/api/tracker')
  },

  addTracker (trackerData) {
    return axios.post('/api/tracker', {
      name: trackerData.name,
      type: trackerData.type,
      info: trackerData.info,
      secret: trackerData.secret
    })
  },

  deleteTracker (trackerId) {
    return axios.delete('/api/tracker/' + trackerId)
  },

  getTracker (trackerId) {
    return axios.get('/api/tracker/' + trackerId)
  },

  updateTracker (trackerInfo) {
    return axios.put('/api/tracker/' + trackerInfo.trackerId, {
      name: '',
      type: '',
      info: '',
      status: ''
    })
  },

  listTrackerProject (trackerId) {
    return axios.get('/api/tracker/' + trackerId + '/projects')
  },

  listTrackerSprint (project) {},

  listTrackerIssueType (project) {
    return axios.get('/api/tracker/' + trackerId + '/issue_types')
  },

  listTrackerIssueStatus (trackerId) {
    return axios.get('/api/tracker/' + trackerId + '/issue_statuses')
  }
}
