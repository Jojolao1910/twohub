<template>
    <div class="dashboard-container">
      <header class="bg-indigo-600 text-white p-4">
        <h1 class="text-2xl font-bold">Dashboard Principal</h1>
      </header>
      <main class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <DashboardCard 
            title="Gerenciamento de Produtos" 
            icon="package" 
            @click="navigateTo('/produtos/gerenciar')"
          />
          <DashboardCard 
            title="Lista de Produtos" 
            icon="list" 
            @click="navigateTo('/produtos/lista')"
          />
          <DashboardCard 
            title="Pedidos em Andamento" 
            icon="shopping-cart" 
            @click="navigateTo('/pedidos/andamento')"
          />
          <DashboardCard 
            title="Dashboard de Atendimento" 
            icon="users" 
            @click="navigateTo('/atendimento')"
          />
        </div>
      </main>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import DashboardCard from '@/components/DashboardCard.vue';
  
  const router = useRouter();
  
  const navigateTo = (path) => {
    router.push(path);
  };
  </script>
  
  <style scoped>
  .dashboard-container {
    min-height: 100vh;
    background-color: #f3f4f6;
  }
  </style>