<template>
  <div class="finance-container">
    <div class="finance-header">
      <h2>收支管理</h2>
      <el-button type="primary" @click="openAddModal">添加记录</el-button>
    </div>

    <div class="filter-section">
      <div class="filter-row">
        <span class="filter-label">当前余额：</span>
        <span class="filter-value" :class="wallet.balance >= 0 ? 'positive' : 'negative'">
          ¥{{ wallet.balance.toFixed(2) }}
        </span>
        <span class="filter-label">总收入：</span>
        <span class="filter-value income">+¥{{ wallet.total_income.toFixed(2) }}</span>
        <span class="filter-label">总支出：</span>
        <span class="filter-value expense">-¥{{ wallet.total_expense.toFixed(2) }}</span>
        <span class="filter-label">正常支出：</span>
        <span class="filter-value">-¥{{ wallet.normal_expense.toFixed(2) }}</span>
        <span class="filter-label">安慰支出：</span>
        <span class="filter-value">-¥{{ wallet.comfort_expense.toFixed(2) }}</span>
        <span class="filter-label">非理性支出：</span>
        <span class="filter-value">-¥{{ wallet.irrational_expense.toFixed(2) }}</span>
      </div>
    </div>

    <el-card class="finance-card">
      <el-table :data="records" stripe>
        <el-table-column prop="date" label="日期" />
        <el-table-column prop="type" label="类型">
          <template #default="{ row }">
            <el-tag :type="row.type === 'income' ? 'success' : 'danger'">
              {{ row.type === 'income' ? '收入' : '支出' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" />
        <el-table-column prop="amount" label="金额">
          <template #default="{ row }">
            <span :class="row.type === 'income' ? 'income' : 'expense'">
              {{ row.type === 'income' ? '+' : '-' }}¥{{ row.amount.toFixed(2) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="备注" />
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
        <el-form-item label="类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio value="income">收入</el-radio>
            <el-radio value="expense">支出</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category">
            <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat" />
          </el-select>
        </el-form-item>
        <el-form-item label="金额" prop="amount">
          <el-input v-model.number="form.amount" placeholder="请输入金额" />
        </el-form-item>
        <el-form-item label="备注" prop="description">
          <el-input v-model="form.description" placeholder="请输入备注" />
        </el-form-item>
        <el-form-item label="日期" prop="date">
          <el-date-picker v-model="form.date" type="date" value-format="YYYY-MM-DD" />
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
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { financeApi } from '../api'

const wallet = ref({ 
  balance: 0, 
  total_income: 0, 
  total_expense: 0,
  normal_expense: 0,
  comfort_expense: 0,
  irrational_expense: 0
})
const records = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const categories = ['工资', '奖金', '投资收益', '其他收入', '餐饮', '交通', '购物', '娱乐', '医疗', '教育', '房租', '其他支出']

const form = ref({
  id: null,
  type: 'expense',
  category: '',
  amount: 0,
  description: '',
  date: new Date().toISOString().split('T')[0]
})

const rules = {
  type: [{ required: true, message: '请选择类型', trigger: 'change' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  amount: [{ required: true, message: '请输入金额', trigger: 'blur' }],
  date: [{ required: true, message: '请选择日期', trigger: 'change' }]
}

const loadWallet = async () => {
  try {
    wallet.value = await financeApi.getWallet()
  } catch (error) {
    ElMessage.error('获取钱包失败')
  }
}

const loadRecords = async () => {
  try {
    records.value = await financeApi.getList()
  } catch (error) {
    ElMessage.error('获取记录失败')
  }
}

const openAddModal = () => {
  isEdit.value = false
  form.value = {
    id: null,
    type: 'expense',
    category: '',
    amount: 0,
    description: '',
    date: new Date().toISOString().split('T')[0]
  }
  dialogVisible.value = true
}

const editRecord = (row) => {
  isEdit.value = true
  form.value = {
    id: row.id,
    type: row.type,
    category: row.category,
    amount: row.amount,
    description: row.description || '',
    date: row.date
  }
  dialogVisible.value = true
}

const saveRecord = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await financeApi.update(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          await financeApi.create(form.value)
          ElMessage.success('添加成功')
        }
        dialogVisible.value = false
        await loadWallet()
        await loadRecords()
      } catch (error) {
        ElMessage.error('保存失败')
      }
    }
  })
}

const deleteRecord = async (row) => {
  try {
    await financeApi.delete(row.id)
    ElMessage.success('删除成功')
    await loadWallet()
    await loadRecords()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

onMounted(async () => {
  await loadWallet()
  await loadRecords()
})
</script>

<style scoped>
.finance-container {
  padding: 20px;
}

.finance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.finance-header h2 {
  margin: 0;
}

.filter-section {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.filter-label {
  font-size: 14px;
  color: #666;
}

.filter-value {
  font-size: 14px;
  font-weight: bold;
}

.filter-value.positive {
  color: #67c23a;
}

.filter-value.negative {
  color: #f56c6c;
}

.filter-value.income {
  color: #67c23a;
}

.filter-value.expense {
  color: #f56c6c;
}

.finance-card {
  height: calc(100% - 100px);
}

.empty-tip {
  text-align: center;
  padding: 40px;
  color: #999;
}

.income {
  color: #67c23a;
  font-weight: bold;
}

.expense {
  color: #f56c6c;
  font-weight: bold;
}
</style>
