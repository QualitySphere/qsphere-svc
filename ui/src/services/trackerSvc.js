import axios from 'axios'

export default {
  listTracker () {
    return axios.get('/api/connection')
  },

  addTracker (trackerInfo) {
    return axios.post('/api/connection', {
      connection_name: trackerInfo.name,
      issue_server: {
        type: trackerInfo.type,
        host: trackerInfo.host,
        account: trackerInfo.user,
        password: trackerInfo.password
      },
      case_server: {
        type: '',
        host: '',
        account: '',
        password: ''
      }
    })
  },

  deleteTracker (trackerId) {
    return axios.delete('/api/connection/' + trackerId)
  },

  getTracker (trackerId) {
    return axios.get('/api/connection/' + trackerId)
  },

  updateTracker (trackerInfo) {
    return axios.put('/api/connection/' + trackerInfo.connection_id, {
      case_server_account: '',
      case_server_host: '',
      case_server_password: '',
      case_server_type: '',
      issue_server_account: trackerInfo.issue_server.account,
      issue_server_host: trackerInfo.issue_server.host,
      issue_server_password: trackerInfo.issue_server.password,
      issue_server_type: trackerInfo.issue_server.type
    })
  }
}
