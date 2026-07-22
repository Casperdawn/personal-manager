<template>
  <div class="weight-loss-container">
    <div class="weight-loss-header">
      <h2>减肥记录</h2>
      <el-button type="primary" @click="openAddModal">添加记录</el-button>
    </div>

    <div class="stats-cards">
      <el-card class="stat-card">
        <div class="stat-title">今日体重</div>
        <div class="stat-value">
          <span class="weight">{{ todayWeight }}</span>
          <span class="unit">kg</span>
        </div>
        <div class="stat-change" :class="weightChangeClass">
          <span>{{ weightChange }}</span>
          <span class="change-label">较昨日</span>
        </div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-title">当前BMI</div>
        <div class="stat-value">
          <span class="bmi">{{ todayBMI }}</span>
        </div>
        <div class="stat-change" :class="bmiChangeClass">
          <span>{{ bmiChange }}</span>
          <span class="change-label">较昨日</span>
        </div>
        <div class="bmi-status" :class="bmiStatusClass">{{ bmiStatus }}</div>
      </el-card>

      <el-card class="stat-card">
        <div class="stat-title">累计减重</div>
        <div class="stat-value">
          <span class="weight">{{ totalLoss }}</span>
          <span class="unit">kg</span>
        </div>
        <div class="stat-info">从{{ initialWeight }}kg减至{{ todayWeight }}kg</div>
      </el-card>
    </div>

    <el-card class="chart-card">
      <h3>最近体重变化趋势</h3>
      <canvas ref="chartRef" class="chart-container"></canvas>
    </el-card>

    <el-card class="records-card">
      <h3>历史记录</h3>
      <el-table :data="records" stripe>
        <el-table-column prop="date" label="日期" />
        <el-table-column prop="weight" label="体重(kg)" />
        <el-table-column label="变化">
          <template #default="{ row }">
            <span :class="getWeightChangeClass(row)">
              <span v-if="getWeightChange(row) < 0" class="arrow">↓</span>
              <span v-else-if="getWeightChange(row) > 0" class="arrow">↑</span>
              {{ getWeightChange(row) !== null ? getWeightChange(row).toFixed(1) + 'kg' : '--' }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="BMI">
          <template #default="{ row }">
            {{ calculateBMI(row.weight, row.height).toFixed(1) }}
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button type="text" @click="editRecord(row)">编辑</el-button>
            <el-button type="text" @click="deleteRecord(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="records.length === 0" class="empty-tip">暂无数据</div>
    </el-card>

    <el-dialog :title="isEdit ? '编辑记录' : '添加记录'" v-model="dialogVisible">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="日期" prop="date">
          <el-date-picker v-model="form.date" type="date" value-format="YYYY-MM-DD" />
        </el-form-item>
        <el-form-item label="体重(kg)" prop="weight">
          <el-input-number v-model="form.weight" :min="30" :max="300" :step="0.1" />
        </el-form-item>
        <el-form-item label="身高(cm)" prop="height">
          <el-input-number v-model="form.height" :min="100" :max="250" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRecord">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { healthApi } from '../api'

const records = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)
const chartRef = ref(null)

const today = new Date().toISOString().split('T')[0]

const form = ref({
  id: null,
  date: today,
  weight: 70,
  height: 170
})

const rules = {
  date: [{ required: true, message: '请选择日期', trigger: 'change' }],
  weight: [{ required: true, message: '请输入体重', trigger: 'blur' }],
  height: [{ required: true, message: '请输入身高', trigger: 'blur' }]
}

const calculateBMI = (weight, height) => {
  const heightInMeters = height / 100
  return weight / (heightInMeters * heightInMeters)
}

const getBMIStatus = (bmi) => {
  if (bmi < 18.5) return '偏瘦'
  if (bmi < 24) return '正常'
  if (bmi < 28) return '超重'
  return '肥胖'
}

const getBMIStatusClass = (bmi) => {
  if (bmi < 18.5) return 'status-underweight'
  if (bmi < 24) return 'status-normal'
  if (bmi < 28) return 'status-overweight'
  return 'status-obese'
}

const sortedRecords = computed(() => {
  return [...records.value].sort((a, b) => new Date(a.date) - new Date(b.date))
})

const todayRecord = computed(() => {
  return records.value.find(r => r.date === today) || records.value[0]
})

const yesterdayRecord = computed(() => {
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  const yesterdayStr = yesterday.toISOString().split('T')[0]
  return records.value.find(r => r.date === yesterdayStr)
})

const todayWeight = computed(() => {
  return todayRecord.value ? todayRecord.value.weight.toFixed(1) : '--'
})

const todayBMI = computed(() => {
  if (!todayRecord.value) return '--'
  return calculateBMI(todayRecord.value.weight, todayRecord.value.height).toFixed(1)
})

const bmiStatus = computed(() => {
  if (!todayRecord.value) return '--'
  return getBMIStatus(calculateBMI(todayRecord.value.weight, todayRecord.value.height))
})

const bmiStatusClass = computed(() => {
  if (!todayRecord.value) return ''
  return getBMIStatusClass(calculateBMI(todayRecord.value.weight, todayRecord.value.height))
})

const weightChange = computed(() => {
  if (!todayRecord.value || !yesterdayRecord.value) return '--'
  const change = todayRecord.value.weight - yesterdayRecord.value.weight
  return change > 0 ? `+${change.toFixed(1)}kg` : `${change.toFixed(1)}kg`
})

const weightChangeClass = computed(() => {
  if (!todayRecord.value || !yesterdayRecord.value) return ''
  const change = todayRecord.value.weight - yesterdayRecord.value.weight
  if (change > 0) return 'change-up'
  if (change < 0) return 'change-down'
  return ''
})

const bmiChange = computed(() => {
  if (!todayRecord.value || !yesterdayRecord.value) return '--'
  const todayBMIValue = calculateBMI(todayRecord.value.weight, todayRecord.value.height)
  const yesterdayBMIValue = calculateBMI(yesterdayRecord.value.weight, yesterdayRecord.value.height)
  const change = todayBMIValue - yesterdayBMIValue
  return change > 0 ? `+${change.toFixed(2)}` : `${change.toFixed(2)}`
})

const bmiChangeClass = computed(() => {
  if (!todayRecord.value || !yesterdayRecord.value) return ''
  const todayBMIValue = calculateBMI(todayRecord.value.weight, todayRecord.value.height)
  const yesterdayBMIValue = calculateBMI(yesterdayRecord.value.weight, yesterdayRecord.value.height)
  const change = todayBMIValue - yesterdayBMIValue
  if (change > 0) return 'change-up'
  if (change < 0) return 'change-down'
  return ''
})

const initialWeight = computed(() => {
  if (sortedRecords.value.length === 0) return '--'
  return sortedRecords.value[0].weight.toFixed(1)
})

const totalLoss = computed(() => {
  if (sortedRecords.value.length === 0 || !todayRecord.value) return '--'
  const loss = sortedRecords.value[0].weight - todayRecord.value.weight
  return loss > 0 ? loss.toFixed(1) : '0.0'
})

const getWeightChange = (row) => {
  const idx = sortedRecords.value.findIndex(r => r.id === row.id)
  if (idx <= 0) return null
  const prevRecord = sortedRecords.value[idx - 1]
  return row.weight - prevRecord.weight
}

const getWeightChangeClass = (row) => {
  const change = getWeightChange(row)
  if (change === null) return ''
  if (change > 0) return 'change-up'
  if (change < 0) return 'change-down'
  return ''
}

const drawChart = () => {
  if (!chartRef.value || sortedRecords.value.length < 2) return
  
  const ctx = chartRef.value.getContext('2d')
  
  const padding = { top: 30, right: 30, bottom: 40, left: 50 }
  const width = chartRef.value.width
  const height = chartRef.value.height
  const chartWidth = width - padding.left - padding.right
  const chartHeight = height - padding.top - padding.bottom
  
  ctx.clearRect(0, 0, width, height)
  
  const weights = sortedRecords.value.map(r => r.weight)
  const dates = sortedRecords.value.map(r => r.date.slice(5))
  
  const minWeight = Math.min(...weights) - 1
  const maxWeight = Math.max(...weights) + 1
  const weightRange = maxWeight - minWeight
  
  ctx.strokeStyle = '#e5e7eb'
  ctx.lineWidth = 1
  for (let i = 0; i <= 5; i++) {
    const y = padding.top + (chartHeight / 5) * i
    ctx.beginPath()
    ctx.moveTo(padding.left, y)
    ctx.lineTo(width - padding.right, y)
    ctx.stroke()
    
    const weight = maxWeight - (weightRange / 5) * i
    ctx.fillStyle = '#6b7280'
    ctx.font = '12px sans-serif'
    ctx.textAlign = 'right'
    ctx.fillText(weight.toFixed(1) + 'kg', padding.left - 10, y + 4)
  }
  
  ctx.fillStyle = '#6b7280'
  ctx.font = '12px sans-serif'
  ctx.textAlign = 'center'
  dates.forEach((date, i) => {
    const x = padding.left + (chartWidth / (dates.length - 1)) * i
    ctx.fillText(date, x, height - 15)
  })
  
  ctx.beginPath()
  ctx.strokeStyle = '#667eea'
  ctx.lineWidth = 3
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  
  weights.forEach((weight, i) => {
    const x = padding.left + (chartWidth / (weights.length - 1)) * i
    const y = padding.top + chartHeight - ((weight - minWeight) / weightRange) * chartHeight
    if (i === 0) {
      ctx.moveTo(x, y)
    } else {
      ctx.lineTo(x, y)
    }
  })
  ctx.stroke()
  
  weights.forEach((weight, i) => {
    const x = padding.left + (chartWidth / (weights.length - 1)) * i
    const y = padding.top + chartHeight - ((weight - minWeight) / weightRange) * chartHeight
    
    ctx.beginPath()
    ctx.fillStyle = '#667eea'
    ctx.arc(x, y, 5, 0, Math.PI * 2)
    ctx.fill()
    
    ctx.beginPath()
    ctx.fillStyle = '#ffffff'
    ctx.arc(x, y, 2, 0, Math.PI * 2)
    ctx.fill()
  })
}

const loadRecords = async () => {
  try {
    records.value = await healthApi.getWeightLossList()
    await nextTick()
    drawChart()
  } catch (error) {
    ElMessage.error('获取记录失败')
  }
}

const openAddModal = () => {
  isEdit.value = false
  form.value = {
    id: null,
    date: today,
    weight: 70,
    height: 170
  }
  dialogVisible.value = true
}

const editRecord = (row) => {
  isEdit.value = true
  form.value = {
    id: row.id,
    date: row.date,
    weight: row.weight,
    height: row.height
  }
  dialogVisible.value = true
}

const saveRecord = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await healthApi.updateWeightLoss(form.value.id, form.value)
          ElMessage.success('更新成功')
          dialogVisible.value = false
          loadRecords()
        } else {
          const existingRecord = records.value.find(r => r.date === form.value.date)
          if (existingRecord) {
            const confirmDialog = await ElMessageBox.confirm(
              '已有记录，是否选择覆盖？',
              '提示',
              {
                confirmButtonText: '确定覆盖',
                cancelButtonText: '取消',
                type: 'warning'
              }
            )
            if (confirmDialog === 'confirm') {
              await healthApi.updateWeightLoss(existingRecord.id, form.value)
              ElMessage.success('覆盖成功')
              dialogVisible.value = false
              loadRecords()
            }
          } else {
            await healthApi.createWeightLoss(form.value)
            ElMessage.success('添加成功')
            dialogVisible.value = false
            loadRecords()
          }
        }
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('保存失败')
        }
      }
    }
  })
}

const deleteRecord = async (row) => {
  try {
    await healthApi.deleteWeightLoss(row.id)
    ElMessage.success('删除成功')
    loadRecords()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  loadRecords()
})
</script>

<style scoped>
.weight-loss-container {
  height: 100%;
}

.weight-loss-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.weight-loss-header h2 {
  margin: 0;
}

.stats-cards {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  flex: 1;
  text-align: center;
}

.stat-title {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #333;
}

.stat-value .unit {
  font-size: 18px;
  font-weight: normal;
  color: #999;
  margin-left: 5px;
}

.stat-change {
  font-size: 14px;
  margin-top: 5px;
}

.change-up {
  color: #ef4444;
}

.change-down {
  color: #22c55e;
}

.change-label {
  margin-left: 5px;
  color: #999;
}

.stat-info {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.bmi-status {
  margin-top: 8px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  display: inline-block;
}

.status-underweight {
  background-color: #dbeafe;
  color: #3b82f6;
}

.status-normal {
  background-color: #dcfce7;
  color: #22c55e;
}

.status-overweight {
  background-color: #fef9c3;
  color: #eab308;
}

.status-obese {
  background-color: #fee2e2;
  color: #ef4444;
}

.chart-card, .records-card {
  margin-bottom: 20px;
}

.chart-card h3, .records-card h3 {
  margin: 0 0 15px 0;
  font-size: 16px;
}

.chart-container {
  width: 100%;
  height: 300px;
}

.empty-tip {
  text-align: center;
  padding: 40px;
  color: #999;
}

.arrow {
  margin-right: 4px;
}
</style>
