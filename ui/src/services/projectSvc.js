import axios from 'axios'

export default {

  listProject () {
    return axios.get('/api/project')
  },

  addProject (projectData) {
    return axios.post('/api/project', projectData)
  }
}
