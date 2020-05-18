import axios from 'axios'

export default {
  listTracker () {
    return axios.get('/api/connection')
  }
}
