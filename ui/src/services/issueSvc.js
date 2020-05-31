import axios from 'axios'

export default {

  syncSprintIssue (sprintId) {
    return axios.get('/api/issue/sync?sprint_id=' + sprintId)
  }
}
