<template>
    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold mb-4">Pedidos em Andamento</h1>
  
      <div class="bg-white shadow-md rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nº do Pedido</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Itens</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Última Atualização</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="order in orders" :key="order.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ order.id }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ order.customerName }}</td>
              <td class="px-6 py-4">
                <ul class="list-disc list-inside">
                  <li v-for="item in order.items" :key="item.id">
                    {{ item.name }} ({{ item.quantity }})
                  </li>
                </ul>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getStatusClass(order.status)">
                  {{ order.status }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {{ formatDate(order.updatedAt) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  import axios from 'axios';
  import io from 'socket.io-client';
  
  const API_URL = 'https://api.example.com/orders';
  const WEBSOCKET_URL = 'wss://api.example.com';
  
  const orders = ref([]);
  let socket = null;
  let intervalId = null;
  
  const fetchOrders = async () => {
    try {
      const response = await axios.get(API_URL);
      orders.value = response.data;
    } catch (error) {
      console.error('Erro ao buscar pedidos:', error);
      // Aqui você pode adicionar uma notificação de erro para o usuário
    }
  };
  
  const setupWebSocket = () => {
    socket = io(WEBSOCKET_URL);
  
    socket.on('connect', () => {
      console.log('Conectado ao WebSocket');
    });
  
    socket.on('orderUpdate', (updatedOrder) => {
      const index = orders.value.findIndex(order => order.id === updatedOrder.id);
      if (index !== -1) {
        orders.value[index] = updatedOrder;
      } else {
        orders.value.push(updatedOrder);
      }
    });
  
    socket.on('disconnect', () => {
      console.log('Desconectado do WebSocket');
    });
  };
  
  const setupPolling = () => {
    intervalId = setInterval(fetchOrders, 30000); // Atualiza a cada 30 segundos
  };
  
  const getStatusClass = (status) => {
    const classes = {
      'Pedido recebido': 'bg-blue-100 text-blue-800',
      'Sendo preparado': 'bg-yellow-100 text-yellow-800',
      'Finalizado': 'bg-green-100 text-green-800',
      'Saiu para entrega': 'bg-purple-100 text-purple-800'
    };
    return `px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${classes[status] || 'bg-gray-100 text-gray-800'}`;
  };
  
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
  };
  
  onMounted(() => {
    fetchOrders();
    
    // Tenta configurar WebSocket primeiro
    setupWebSocket();
    
    // Se o WebSocket falhar, configura polling como fallback
    if (!socket || !socket.connected) {
      console.log('WebSocket não disponível, usando polling como fallback');
      setupPolling();
    }
  });
  
  onUnmounted(() => {
    if (socket) {
      socket.disconnect();
    }
    if (intervalId) {
      clearInterval(intervalId);
    }
  });
  </script>