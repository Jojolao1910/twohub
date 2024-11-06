<template>
    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold mb-4">Dashboard de Atendimento</h1>
  
      <!-- Filtros de data e hora -->
      <div class="mb-4 flex flex-wrap gap-4">
        <div>
          <label for="date" class="block text-sm font-medium text-gray-700">Data</label>
          <input
            type="date"
            id="date"
            v-model="filters.date"
            @change="updateData"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          >
        </div>
        <div>
          <label for="month" class="block text-sm font-medium text-gray-700">Mês</label>
          <input
            type="month"
            id="month"
            v-model="filters.month"
            @change="updateData"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          >
        </div>
        <div>
          <label for="year" class="block text-sm font-medium text-gray-700">Ano</label>
          <input
            type="number"
            id="year"
            v-model="filters.year"
            @change="updateData"
            min="2000"
            :max="new Date().getFullYear()"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          >
        </div>
        <div>
          <label for="hour" class="block text-sm font-medium text-gray-700">Hora</label>
          <input
            type="time"
            id="hour"
            v-model="filters.hour"
            @change="updateData"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
          >
        </div>
      </div>
  
      <!-- Gráfico de atendimento -->
      <div class="bg-white p-4 rounded-lg shadow-md">
        <canvas ref="chartRef"></canvas>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted, reactive } from 'vue';
  import Chart from 'chart.js/auto';
  import io from 'socket.io-client';
  import axios from 'axios';
  
  const API_URL = 'https://api.example.com/support-data';
  const WEBSOCKET_URL = 'wss://api.example.com';
  
  const chartRef = ref(null);
  let chart = null;
  let socket = null;
  let intervalId = null;
  
  const filters = reactive({
    date: new Date().toISOString().split('T')[0],
    month: new Date().toISOString().slice(0, 7),
    year: new Date().getFullYear(),
    hour: ''
  });
  
  const chartData = reactive({
    labels: ['Recebidas', 'Atendidas', 'Finalizadas', 'Não Concluídas'],
    datasets: [{
      label: 'Atendimentos',
      data: [0, 0, 0, 0],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(255, 206, 86, 0.2)'
      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(255, 206, 86, 1)'
      ],
      borderWidth: 1
    }]
  });
  
  const createChart = () => {
    const ctx = chartRef.value.getContext('2d');
    chart = new Chart(ctx, {
      type: 'bar',
      data: chartData,
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
  };
  
  const updateChart = (newData) => {
    chartData.datasets[0].data = newData;
    chart.update();
  };
  
  const fetchData = async () => {
    try {
      const response = await axios.get(API_URL, { params: filters });
      updateChart(response.data);
    } catch (error) {
      console.error('Erro ao buscar dados de atendimento:', error);
      // Adicionar uma notificação de erro para o usuário
    }
  };
  
  const setupWebSocket = () => {
    socket = io(WEBSOCKET_URL);
  
    socket.on('connect', () => {
      console.log('Conectado ao WebSocket');
    });
  
    socket.on('supportDataUpdate', (newData) => {
      updateChart(newData);
    });
  
    socket.on('disconnect', () => {
      console.log('Desconectado do WebSocket');
    });
  };
  
  const setupPolling = () => {
    intervalId = setInterval(fetchData, 30000); // Atualiza a cada 30 segundos
  };
  
  const updateData = () => {
    fetchData();
    if (socket && socket.connected) {
      socket.emit('updateFilters', filters);
    }
  };
  
  onMounted(() => {
    createChart();
    fetchData();
    
    // Tenta configurar WebSocket primeiro
    setupWebSocket();
    
    // Se o WebSocket falhar, configura polling como fallback
    if (!socket || !socket.connected) {
      console.log('WebSocket não disponível, usando polling como fallback');
      setupPolling();
    }
  });
  
  onUnmounted(() => {
    if (chart) {
      chart.destroy();
    }
    if (socket) {
      socket.disconnect();
    }
    if (intervalId) {
      clearInterval(intervalId);
    }
  });
  </script>