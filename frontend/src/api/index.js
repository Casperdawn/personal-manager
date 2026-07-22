import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

api.interceptors.response.use(response => {
  return response.data
}, error => {
  if (error.response && error.response.status === 401) {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    window.location.href = '/login'
  }
  return Promise.reject(error)
})

export const authApi = {
  register(data) {
    return api.post('/auth/register', data)
  },
  login(data) {
    return api.post('/auth/login', data, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },
  getMe() {
    return api.get('/auth/me')
  }
}

export const todoApi = {
  getList(params) {
    return api.get('/todo/', { params })
  },
  getById(id) {
    return api.get(`/todo/${id}`)
  },
  create(data) {
    return api.post('/todo/', data)
  },
  update(id, data) {
    return api.put(`/todo/${id}`, data)
  },
  delete(id) {
    return api.delete(`/todo/${id}`)
  }
}

export const financeApi = {
  getList(params) {
    return api.get('/finance/', { params })
  },
  getById(id) {
    return api.get(`/finance/${id}`)
  },
  create(data) {
    return api.post('/finance/', data)
  },
  update(id, data) {
    return api.put(`/finance/${id}`, data)
  },
  delete(id) {
    return api.delete(`/finance/${id}`)
  },
  getWallet() {
    return api.get('/finance/wallet')
  },
  getYears() {
    return api.get('/finance/years')
  },
  getMonthlyStats(year) {
    return api.get('/finance/monthly-stats', { params: { year } })
  },
  getDailyStats(year, month) {
    return api.get(`/finance/daily-stats/${year}/${month}`)
  },
  getDailyDetails(date) {
    return api.get(`/finance/daily-details/${date}`)
  }
}

export const learningApi = {
  getList(params) {
    return api.get('/learning/', { params })
  },
  getById(id) {
    return api.get(`/learning/${id}`)
  },
  create(data) {
    return api.post('/learning/', data)
  },
  update(id, data) {
    return api.put(`/learning/${id}`, data)
  },
  delete(id) {
    return api.delete(`/learning/${id}`)
  }
}

export const healthApi = {
  getWeightLossList(params) {
    return api.get('/health/weight-loss/', { params })
  },
  getWeightLossById(id) {
    return api.get(`/health/weight-loss/${id}`)
  },
  createWeightLoss(data) {
    return api.post('/health/weight-loss/', data)
  },
  updateWeightLoss(id, data) {
    return api.put(`/health/weight-loss/${id}`, data)
  },
  deleteWeightLoss(id) {
    return api.delete(`/health/weight-loss/${id}`)
  }
}

export default api
