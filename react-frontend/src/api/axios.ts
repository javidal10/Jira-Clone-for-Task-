import axios from 'axios'

const axiosDf = axios.create({
	baseURL: 'http://localhost:8000/api/',
})

export default axiosDf
