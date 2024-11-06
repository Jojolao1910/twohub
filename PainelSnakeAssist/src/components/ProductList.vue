<template>
    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold mb-4">Lista de Produtos</h1>
  
      <!-- Barra de busca -->
      <div class="mb-4">
        <input
          v-model="searchQuery"
          @input="debouncedSearch"
          type="text"
          placeholder="Buscar produtos..."
          class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
        >
      </div>
  
      <!-- Tabela de Produtos -->
      <div class="bg-white shadow-md rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Preço</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estoque</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descrição</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="product in products" :key="product.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ product.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap">R$ {{ product.price.toFixed(2) }}</td>
              <td class="px-6 py-4 whitespace-nowrap">{{ product.stock }}</td>
              <td class="px-6 py-4">
                <p class="text-sm text-gray-900 truncate max-w-xs">{{ product.description }}</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Paginação -->
      <div class="mt-4 flex justify-between items-center">
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
        >
          Anterior
        </button>
        <span class="text-sm text-gray-700">
          Página {{ currentPage }} de {{ totalPages }}
        </span>
        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
        >
          Próxima
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import axios from 'axios';
  import debounce from 'lodash/debounce';
  
  const API_URL = 'https://api.example.com/products'; // Substitua pela URL real da sua API
  const products = ref([]);
  const currentPage = ref(1);
  const totalPages = ref(1);
  const itemsPerPage = 10; // Ajuste conforme necessário
  const searchQuery = ref('');
  
  const fetchProducts = async (page = 1, search = '') => {
    try {
      const response = await axios.get(API_URL, {
        params: {
          page,
          limit: itemsPerPage,
          search
        }
      });
      products.value = response.data.products;
      totalPages.value = response.data.totalPages;
      currentPage.value = page;
    } catch (error) {
      console.error('Erro ao buscar produtos:', error);
      // Aqui você pode adicionar uma notificação de erro para o usuário
    }
  };
  
  const debouncedSearch = debounce(() => {
    currentPage.value = 1; // Reset para a primeira página ao buscar
    fetchProducts(1, searchQuery.value);
  }, 300);
  
  const prevPage = () => {
    if (currentPage.value > 1) {
      fetchProducts(currentPage.value - 1, searchQuery.value);
    }
  };
  
  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      fetchProducts(currentPage.value + 1, searchQuery.value);
    }
  };
  
  onMounted(() => {
    fetchProducts();
  });
  </script>