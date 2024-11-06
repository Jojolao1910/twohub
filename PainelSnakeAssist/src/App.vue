<template>
  <div id="app">
    <!-- Navigation component  -->
    <nav v-if="authStore.isAuthenticated">
      <!-- Adicione links de navegação aqui -->
    </nav>

    <!-- Router view component -->
    <router-view></router-view>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  // Verificar se há um token salvo e redirecionar se necessário
  const savedToken = localStorage.getItem('token')
  if (savedToken) {
    authStore.setToken(savedToken)
    // Validar o token aqui
    // e buscar informações do usuário do backend
  } else {
    // Se não houver token, redirecione para a página de login
    router.push('/login')
  }
})
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

/* Adicione estilos globais adicionais aqui */
</style>