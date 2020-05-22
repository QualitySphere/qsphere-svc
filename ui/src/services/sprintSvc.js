import axios from 'axios'

export default {
  listSprint () {
    return axios.get('/api/sprint')
  },
  addSprint (sprintData) {
    return axios.post('/api/sprint', sprintData)
  }
}
