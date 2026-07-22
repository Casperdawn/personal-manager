<template>
  <div class="learning-container">
    <div class="learning-header">
      <h2>{{ pageTitle }}</h2>
      <el-button type="primary" @click="openAddModal">添加项目</el-button>
    </div>

    <el-card class="learning-card">
      <el-table :data="records" stripe>
        <el-table-column prop="project" label="学习项目" />
        <el-table-column prop="outline" label="大纲" show-overflow-tooltip />
        <el-table-column prop="estimated_duration" label="预计学习时长">
          <template #default="{ row }">
            {{ formatDuration(row.estimated_duration) }}
          </template>
        </el-table-column>
        <el-table-column prop="accumulated_duration" label="累计学习时长">
          <template #default="{ row }">
            {{ formatDuration(row.accumulated_duration) }}
          </template>
        </el-table-column>
        <el-table-column prop="progress" label="进度">
          <template #default="{ row }">
            <el-progress :percentage="row.progress" :stroke-width="12" />
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" />
        <el-table-column label="预计完成日期">
          <template #default="{ row }">
            {{ getEstimatedCompletionDate(row) }}
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button type="text" @click="editRecord(row)">编辑</el-button>
            <el-button type="text" @click="showDeleteConfirm(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="isEdit ? '编辑记录' : '添加记录'" v-model="dialogVisible">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="140px">
        <el-form-item label="学习项目" prop="project">
          <el-input v-model="form.project" placeholder="请输入学习项目" />
        </el-form-item>
        <el-form-item label="大纲" prop="outline">
          <el-input v-model="form.outline" type="textarea" placeholder="请输入大纲" :rows="3" />
        </el-form-item>
        <el-form-item label="预计学习时长" prop="estimated_duration">
          <el-input-number v-model="form.estimated_duration" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="累计学习时长" prop="accumulated_duration">
          <el-input-number v-model="form.accumulated_duration" :min="0" style="width: 100%" />
        </el-form-item>
        <el-form-item label="进度(%)" prop="progress">
          <el-input-number v-model="form.progress" :min="0" :max="100" style="width: 100%" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="form.start_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRecord">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog title="确认删除" v-model="deleteDialogVisible">
      <p>确定要删除"{{ deleteRecordData?.project }}"吗？</p>
      <template #footer>
        <el-button @click="deleteDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmDelete">确定删除</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { learningApi } from '../api'

const route = useRoute()
const records = ref([])
const dialogVisible = ref(false)
const deleteDialogVisible = ref(false)
const deleteRecordData = ref(null)
const isEdit = ref(false)
const formRef = ref(null)

const today = new Date().toISOString().split('T')[0]

const currentCategory = computed(() => {
  const path = route.path
  if (path.includes('computer')) return '计算机'
  if (path.includes('math')) return '数学'
  if (path.includes('english')) return '英语'
  return '学习'
})

const pageTitle = computed(() => {
  return `${currentCategory.value}学习`
})

const form = ref({
  id: null,
  project: '',
  category: '',
  outline: '',
  estimated_duration: 0,
  accumulated_duration: 0,
  progress: 0,
  start_date: today
})

const rules = {
  project: [{ required: true, message: '请输入学习项目', trigger: 'blur' }],
  estimated_duration: [{ required: true, message: '请输入预计学习时长', trigger: 'blur' }],
  start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }]
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

const getEstimatedCompletionDate = (row) => {
  if (!row.start_date || row.progress <= 0) return '--'
  
  const start = new Date(row.start_date)
  const currentDate = new Date()
  const daysPassed = Math.floor((currentDate - start) / (1000 * 60 * 60 * 24))
  
  if (daysPassed <= 0) return '--'
  
  const progressPerDay = row.progress / daysPassed
  const totalDaysNeeded = 100 / progressPerDay
  const remainingDays = Math.ceil(totalDaysNeeded - daysPassed)
  
  const completionDate = new Date(start)
  completionDate.setDate(start.getDate() + Math.ceil(totalDaysNeeded))
  
  const year = completionDate.getFullYear()
  const month = String(completionDate.getMonth() + 1).padStart(2, '0')
  const day = String(completionDate.getDate()).padStart(2, '0')
  
  return `${year}-${month}-${day}`
}

const loadRecords = async () => {
  try {
    records.value = await learningApi.getList({ category: currentCategory.value })
  } catch (error) {
    ElMessage.error('获取记录失败')
  }
}

const openAddModal = () => {
  isEdit.value = false
  form.value = {
    id: null,
    project: '',
    category: currentCategory.value,
    outline: '',
    estimated_duration: 0,
    accumulated_duration: 0,
    progress: 0,
    start_date: today
  }
  dialogVisible.value = true
}

const editRecord = (row) => {
  isEdit.value = true
  form.value = {
    id: row.id,
    project: row.project,
    category: row.category,
    outline: row.outline || '',
    estimated_duration: row.estimated_duration,
    accumulated_duration: row.accumulated_duration,
    progress: row.progress,
    start_date: row.start_date
  }
  dialogVisible.value = true
}

const saveRecord = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await learningApi.update(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          await learningApi.create(form.value)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        loadRecords()
      } catch (error) {
        ElMessage.error('保存失败')
      }
    }
  })
}

const showDeleteConfirm = (row) => {
  deleteRecordData.value = row
  deleteDialogVisible.value = true
}

const confirmDelete = async () => {
  if (!deleteRecordData.value) return
  try {
    await learningApi.delete(deleteRecordData.value.id)
    ElMessage.success('删除成功')
    deleteDialogVisible.value = false
    loadRecords()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(() => {
  loadRecords()
})

watch(() => route.path, () => {
  loadRecords()
})
</script>

<style scoped>
.learning-container {
  height: 100%;
}

.learning-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.learning-header h2 {
  margin: 0;
}

.learning-card {
  height: calc(100% - 60px);
}
</style>
