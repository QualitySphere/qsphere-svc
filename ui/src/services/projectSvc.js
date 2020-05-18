import axios from 'axios'

export default {
  listProject () {
    return axios.get('/api/project')
  }
}
