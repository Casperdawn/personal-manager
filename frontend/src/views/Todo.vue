<template>
  <div class="todo-container">
    <div class="todo-header">
      <h2>{{ pageTitle }}</h2>
      <el-button type="primary" @click="openAddModal">添加{{ currentView === 'tasks' ? '事务' : '小事' }}</el-button>
    </div>

    <div class="filter-section">
      <div class="filter-row">
        <span class="filter-label">日期：</span>
        <el-date-picker
          v-model="filterDate"
          type="date"
          placeholder="选择日期"
          value-format="YYYY-MM-DD"
          @change="handleFilter"
        />
        <span class="filter-label">完成状态：</span>
        <el-select v-model="filterCompleted" @change="handleFilter">
          <el-option label="全部" :value="'all'" />
          <el-option label="已完成" :value="true" />
          <el-option label="未完成" :value="false" />
        </el-select>
        <el-button type="primary" @click="handleFilter">搜索</el-button>
        <el-button type="default" @click="resetFilter">重置筛选</el-button>
      </div>
    </div>

    <el-card class="todo-card">
      <el-table :data="filteredTodos" stripe>
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="content" label="内容" />
        <el-table-column prop="date" label="日期" />
        <el-table-column prop="priority" label="优先级">
          <template #default="{ row }">
            <el-tag :type="getPriorityType(row.priority)">
              {{ getPriorityText(row.priority) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="completed" label="状态">
          <template #default="{ row }">
            <div 
              class="status-icon" 
              :class="{ completed: row.completed }"
              @click="toggleComplete(row)"
            >
              <span v-if="row.completed" class="check-icon">✓</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" />
        <el-table-column prop="duration" label="时长">
          <template #default="{ row }">
            {{ formatDuration(row.duration) }}
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button type="text" @click="editTodo(row)">编辑</el-button>
            <el-button type="text" @click="showDeleteConfirm(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="filteredTodos.length === 0" class="empty-tip">暂无数据</div>
    </el-card>

    <el-dialog :title="isEdit ? '编辑事项' : '添加事项'" v-model="dialogVisible">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" type="textarea" placeholder="请输入内容" />
        </el-form-item>
        <el-form-item label="日期" prop="date">
          <el-date-picker v-model="form.date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="form.priority">
            <el-option 
              v-for="item in allowedPriorities" 
              :key="item.value" 
              :label="item.label" 
              :value="item.value" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="完成状态" prop="completed">
          <el-select v-model="form.completed">
            <el-option label="未完成" :value="false" />
            <el-option label="已完成" :value="true" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-time-picker
            v-model="form.start_time"
            type="time"
            placeholder="选择开始时间"
            value-format="HH:mm"
          />
        </el-form-item>
        <el-form-item label="时长(分钟)" prop="duration">
          <el-input-number
            v-model="form.duration"
            :min="1"
            :max="1440"
            placeholder="请输入时长"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTodo">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog title="确认删除" v-model="deleteConfirmVisible">
      <p>确定要删除事项「{{ deleteRow?.title }}」吗？</p>
      <template #footer>
        <el-button @click="deleteConfirmVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmDelete">确认删除</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { todoApi } from '../api'

const route = useRoute()
const todos = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const today = new Date().toISOString().split('T')[0]
const filterDate = ref(today)
const filterCompleted = ref('all')
const filterPriority = ref('all')

const currentView = computed(() => {
  const path = route.path
  if (path.includes('tasks') && !path.includes('small-tasks')) {
    return 'tasks'
  } else if (path.includes('small-tasks')) {
    return 'small-tasks'
  }
  return 'tasks'
})

const pageTitle = computed(() => {
  return currentView.value === 'tasks' ? '每日事务' : '每日小事'
})

const allowedPriorities = computed(() => {
  return currentView.value === 'tasks' 
    ? [{ label: '高', value: 3 }]
    : [{ label: '低', value: 1 }, { label: '中', value: 2 }]
})

const defaultPriority = computed(() => {
  return currentView.value === 'tasks' ? 3 : 1
})

const deleteConfirmVisible = ref(false)
const deleteRow = ref(null)

const getCurrentTime = () => {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  return `${hours}:${minutes}`
}

const form = ref({
  id: null,
  title: '',
  content: '',
  priority: 1,
  date: today,
  completed: false,
  start_time: '',
  duration: 45
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }]
}

const formatDate = (date) => {
  if (date instanceof Date) {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
  }
  return date
}

const formatDuration = (minutes) => {
  if (!minutes || minutes <= 0) return ''
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  if (hours > 0 && mins > 0) {
    return `${hours}h${mins}min`
  } else if (hours > 0) {
    return `${hours}h`
  } else {
    return `${mins}min`
  }
}

const filteredTodos = computed(() => {
  let result = todos.value
  const currentFilterDate = formatDate(filterDate.value)
  if (currentFilterDate) {
    result = result.filter(t => t.date === currentFilterDate)
  }
  if (currentView.value === 'tasks') {
    result = result.filter(t => t.priority === 3)
  } else {
    result = result.filter(t => t.priority === 1 || t.priority === 2)
  }
  if (filterCompleted.value !== 'all') {
    result = result.filter(t => t.completed === filterCompleted.value)
  }
  result.sort((a, b) => b.priority - a.priority)
  return result
})

const getPriorityType = (level) => {
  const types = { 1: 'info', 2: 'warning', 3: 'danger' }
  return types[level] || 'info'
}

const getPriorityText = (level) => {
  const texts = { 1: '低', 2: '中', 3: '高' }
  return texts[level] || '低'
}

const loadTodos = async () => {
  try {
    todos.value = await todoApi.getList()
  } catch (error) {
    ElMessage.error('获取事项失败')
  }
}

const handleFilter = () => {
}

const resetFilter = () => {
  filterDate.value = today
  filterCompleted.value = 'all'
  filterPriority.value = 'all'
}

const openAddModal = () => {
  isEdit.value = false
  form.value = { 
    id: null, 
    title: '', 
    content: '', 
    priority: defaultPriority.value,
    date: today,
    completed: false,
    start_time: getCurrentTime(),
    duration: 45
  }
  dialogVisible.value = true
}

const editTodo = (row) => {
  isEdit.value = true
  form.value = {
    id: row.id,
    title: row.title,
    content: row.content || '',
    priority: row.priority,
    date: row.date || today,
    completed: row.completed || false,
    start_time: row.start_time || '',
    duration: row.duration || 45
  }
  dialogVisible.value = true
}

const saveTodo = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await todoApi.update(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          await todoApi.create(form.value)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        loadTodos()
      } catch (error) {
        ElMessage.error('保存失败')
      }
    }
  })
}

const toggleComplete = async (row) => {
  try {
    await todoApi.update(row.id, { completed: !row.completed })
    ElMessage.success('状态已更新')
    loadTodos()
  } catch (error) {
    ElMessage.error('更新失败')
    loadTodos()
  }
}

const showDeleteConfirm = (row) => {
  deleteRow.value = row
  deleteConfirmVisible.value = true
}

const confirmDelete = async () => {
  if (!deleteRow.value) return
  try {
    await todoApi.delete(deleteRow.value.id)
    ElMessage.success('删除成功')
    deleteConfirmVisible.value = false
    loadTodos()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  loadTodos()
})

watch(() => route.path, () => {
  loadTodos()
})
</script>

<style scoped>
.todo-container {
  height: 100%;
}

.todo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.todo-header h2 {
  margin: 0;
}

.filter-section {
  margin-bottom: 20px;
  padding: 15px 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.filter-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.filter-label {
  font-weight: 500;
  color: #666;
}

.filter-row .el-date-picker,
.filter-row .el-select {
  width: 150px;
}

.todo-card {
  height: calc(100% - 120px);
}

.empty-tip {
  text-align: center;
  padding: 40px;
  color: #999;
}

.status-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 2px solid #d9d9d9;
  cursor: pointer;
  transition: all 0.3s ease;
}

.status-icon.completed {
  background-color: #67c23a;
  border-color: #67c23a;
}

.check-icon {
  color: white;
  font-size: 14px;
  font-weight: bold;
}
</style>
