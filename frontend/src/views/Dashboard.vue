<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2>欢迎回来，{{ user?.username }}</h2>
      <p>{{ currentDate }}</p>
    </div>

    <div class="stats-grid">
      <el-card class="stat-card" @click="goToTodo">
        <div class="stat-icon todo-icon">
          <el-icon><List /></el-icon>
        </div>
        <div class="stat-info">
          <h3>每日事项</h3>
          <p class="stat-value">{{ todoStats.total }}</p>
          <p class="stat-label">待完成: {{ todoStats.pending }}</p>
        </div>
        <div class="stat-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
      </el-card>

      <el-card class="stat-card" @click="goToFinance">
        <div class="stat-icon finance-icon">
          <el-icon><Wallet /></el-icon>
        </div>
        <div class="stat-info">
          <h3>收支管理</h3>
          <p class="stat-value income">+{{ financeStats.income.toFixed(2) }}</p>
          <p class="stat-label">支出: -{{ financeStats.expense.toFixed(2) }}</p>
        </div>
        <div class="stat-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
      </el-card>

      <el-card class="stat-card" @click="goToLearning">
        <div class="stat-icon learning-icon">
          <el-icon><Notebook /></el-icon>
        </div>
        <div class="stat-info">
          <h3>学习进度</h3>
          <p class="stat-value">{{ learningStats.totalHours }}h</p>
          <p class="stat-label">今日学习: {{ learningStats.todayMinutes }}分钟</p>
        </div>
        <div class="stat-arrow">
          <el-icon><ArrowRight /></el-icon>
        </div>
      </el-card>
    </div>

    <div class="recent-section">
      <h3>最近事项</h3>
      <el-card class="recent-card">
        <el-table :data="recentTodos" stripe size="small">
          <el-table-column prop="title" label="标题" />
          <el-table-column prop="completed" label="状态">
            <template #default="{ row }">
              <el-tag :type="row.completed ? 'success' : 'warning'">
                {{ row.completed ? '已完成' : '进行中' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" />
        </el-table>
        <div v-if="recentTodos.length === 0" class="empty-tip">
          暂无事项，点击上方卡片开始添加
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { List, Wallet, Notebook, ArrowRight } from '@element-plus/icons-vue'
import { todoApi } from '../api'

const router = useRouter()
const user = ref(null)
const recentTodos = ref([])

const todoStats = ref({ total: 0, pending: 0 })
const financeStats = ref({ income: 0, expense: 0 })
const learningStats = ref({ totalHours: 0, todayMinutes: 0 })

const currentDate = computed(() => {
  const now = new Date()
  return `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日 ${['周日', '周一', '周二', '周三', '周四', '周五', '周六'][now.getDay()]}`
})

onMounted(async () => {
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    user.value = JSON.parse(savedUser)
  }
  
  try {
    const todos = await todoApi.getList({ limit: 5 })
    recentTodos.value = todos
    todoStats.value = {
      total: todos.length,
      pending: todos.filter(t => !t.completed).length
    }
  } catch (error) {
    console.error('获取数据失败:', error)
  }
})

const goToTodo = () => {
  router.push('/todo')
}

const goToFinance = () => {
  router.push('/finance')
}

const goToLearning = () => {
  router.push('/learning')
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.dashboard-header {
  margin-bottom: 30px;
}

.dashboard-header h2 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.dashboard-header p {
  margin: 5px 0 0;
  color: #999;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  padding: 24px;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 28px;
  margin-right: 20px;
}

.todo-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.finance-icon {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
  color: white;
}

.learning-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-info h3 {
  margin: 0;
  font-size: 16px;
  color: #666;
}

.stat-value {
  margin: 8px 0 4px;
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.stat-value.income {
  color: #67c23a;
}

.stat-label {
  margin: 0;
  font-size: 12px;
  color: #999;
}

.stat-arrow {
  color: #ccc;
  font-size: 20px;
}

.recent-section h3 {
  margin: 0 0 15px;
  font-size: 18px;
  color: #333;
}

.recent-card {
  min-height: 200px;
}

.empty-tip {
  text-align: center;
  padding: 40px;
  color: #999;
}
</style>
