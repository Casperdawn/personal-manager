<template>
  <el-container style="height: 100vh;">
    <el-aside width="200px" class="sidebar">
      <div class="logo">个人管理系统</div>
      <el-menu
        :default-active="activeMenu"
        class="menu"
        router
      >
        <el-menu-item index="/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-sub-menu index="/todo">
          <template #title>
            <el-icon><List /></el-icon>
            <span>每日事项</span>
          </template>
          <el-menu-item index="/todo/tasks">每日事务</el-menu-item>
          <el-menu-item index="/todo/small-tasks">每日小事</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="/learning">
          <template #title>
            <el-icon><Notebook /></el-icon>
            <span>学习</span>
          </template>
          <el-menu-item index="/learning/computer">计算机</el-menu-item>
          <el-menu-item index="/learning/math">数学</el-menu-item>
          <el-menu-item index="/learning/english">英语</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="/health">
          <template #title>
            <el-icon><User /></el-icon>
            <span>健康</span>
          </template>
          <el-menu-item index="/health/weight-loss">减肥</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/finance">
          <el-icon><Wallet /></el-icon>
          <span>收支管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="user-info">
          <span>{{ user?.username || '用户' }}</span>
          <el-button type="text" @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { HomeFilled, List, Wallet, Notebook, User } from '@element-plus/icons-vue'
import { authApi } from '../api'

const router = useRouter()
const route = useRoute()
const user = ref(null)

const activeMenu = computed(() => route.path)

onMounted(async () => {
  try {
    const savedUser = localStorage.getItem('user')
    if (savedUser) {
      user.value = JSON.parse(savedUser)
    } else {
      const res = await authApi.getMe()
      user.value = res
      localStorage.setItem('user', JSON.stringify(res))
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
})

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  ElMessage.success('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.sidebar {
  background: #f8f9fa;
  border-right: 1px solid #e9ecef;
}

.logo {
  padding: 24px 20px;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
  color: #333;
  border-bottom: 1px solid #e9ecef;
}

.menu {
  border-right: none;
  margin-top: 10px;
}

.menu :deep(.el-menu-item) {
  color: #555;
  height: 50px;
  line-height: 50px;
}

.menu :deep(.el-menu-item:hover) {
  background: #e9ecef;
  color: #333;
}

.menu :deep(.el-menu-item.is-active) {
  background: #667eea;
  color: white;
}

.header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  background: white;
  border-bottom: 1px solid #eee;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.main-content {
  padding: 20px;
  background: #f5f5f5;
}
</style>
