import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard.vue'
import Todo from '../views/Todo.vue'
import Finance from '../views/Finance.vue'
import Learning from '../views/Learning.vue'
import WeightLoss from '../views/WeightLoss.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/',
      name: 'Layout',
      component: Layout,
      redirect: '/dashboard',
      children: [
        {
          path: '/dashboard',
          name: 'Dashboard',
          component: Dashboard
        },
        {
          path: '/todo',
          name: 'Todo',
          component: Todo,
          children: [
            {
              path: 'tasks',
              name: 'TodoTasks',
              component: Todo
            },
            {
              path: 'small-tasks',
              name: 'TodoSmallTasks',
              component: Todo
            }
          ]
        },
        {
          path: '/finance',
          name: 'Finance',
          component: Finance
        },
        {
          path: '/learning',
          name: 'Learning',
          component: Learning,
          children: [
            {
              path: 'computer',
              name: 'LearningComputer',
              component: Learning
            },
            {
              path: 'math',
              name: 'LearningMath',
              component: Learning
            },
            {
              path: 'english',
              name: 'LearningEnglish',
              component: Learning
            }
          ]
        },
        {
          path: '/health/weight-loss',
          name: 'WeightLoss',
          component: WeightLoss
        }
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.name !== 'Login' && to.name !== 'Register' && !token) {
    next({ name: 'Login' })
  } else {
    next()
  }
})

export default router
