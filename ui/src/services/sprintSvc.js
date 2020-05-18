import axios from 'axios'

export default {
  listSprint () {
    return axios.get('/api/sprint')
  }
}
