<template>
    <div class="container mx-auto p-4">
      <h1 class="text-2xl font-bold mb-4">Gerenciamento de Produtos</h1>
  
      <!-- Formulário de Produto -->
      <form @submit.prevent="handleSubmit" class="mb-8 bg-white p-6 rounded-lg shadow-md">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">Nome do Produto</label>
            <input
              id="name"
              v-model="productForm.name"
              type="text"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            >
          </div>
          <div>
            <label for="price" class="block text-sm font-medium text-gray-700">Preço</label>
            <input
              id="price"
              v-model="productForm.price"
              type="number"
              step="0.01"
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            >
          </div>
          <div class="md:col-span-2">
            <label for="description" class="block text-sm font-medium text-gray-700">Descrição</label>
            <textarea
              id="description"
              v-model="productForm.description"
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"
            ></textarea>
          </div>
        </div>
        <div class="mt-4">
          <button
            type="submit"
            class="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            {{ isEditing ? 'Atualizar Produto' : 'Adicionar Produto' }}
          </button>
          <button
            v-if="isEditing"
            type="button"
            @click="cancelEdit"
            class="ml-2 px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            Cancelar Edição
          </button>
        </div>
      </form>
  
      <!-- Tabela de Produtos -->
      <div class="bg-white shadow-md rounded-lg overflow-hidden">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nome</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Preço</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Descrição</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="product in products" :key="product.id">
              <td class="px-6 py-4 whitespace-nowrap">{{ product.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap">R$ {{ product.price.toFixed(2) }}</td>
              <td class="px-6 py-4">{{ product.description }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button @click="editProduct(product)" class="text-indigo-600 hover:text-indigo-900 mr-2">Editar</button>
                <button @click="deleteProduct(product.id)" class="text-red-600 hover:text-red-900">Excluir</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue';
  import axios from 'axios';
  
  const products = ref([]);
  const isEditing = ref(false);
  const editingProductId = ref(null);
  
  const productForm = reactive({
    name: '',
    price: '',
    description: ''
  });
  
  const API_URL = 'https://api.example.com/products'; // Substitua pela URL real da sua API
  
  onMounted(async () => {
    await fetchProducts();
  });
  
  const fetchProducts = async () => {
    try {
      const response = await axios.get(API_URL);
      products.value = response.data;
    } catch (error) {
      console.error('Erro ao buscar produtos:', error);
      // Aqui você pode adicionar uma notificação de erro para o usuário
    }
  };
  
  const handleSubmit = async () => {
    try {
      if (isEditing.value) {
        await axios.put(`${API_URL}/${editingProductId.value}`, productForm);
      } else {
        await axios.post(API_URL, productForm);
      }
      await fetchProducts();
      resetForm();
      // Aqui você pode adicionar uma notificação de sucesso para o usuário
    } catch (error) {
      console.error('Erro ao salvar produto:', error);
      // Aqui você pode adicionar uma notificação de erro para o usuário
    }
  };
  
  const editProduct = (product) => {
    productForm.name = product.name;
    productForm.price = product.price;
    productForm.description = product.description;
    isEditing.value = true;
    editingProductId.value = product.id;
  };
  
  const cancelEdit = () => {
    resetForm();
  };
  
  const deleteProduct = async (productId) => {
    if (confirm('Tem certeza que deseja excluir este produto?')) {
      try {
        await axios.delete(`${API_URL}/${productId}`);
        await fetchProducts();
        // Aqui você pode adicionar uma notificação de sucesso para o usuário
      } catch (error) {
        console.error('Erro ao excluir produto:', error);
        // Aqui você pode adicionar uma notificação de erro para o usuário
      }
    }
  };
  
  const resetForm = () => {
    productForm.name = '';
    productForm.price = '';
    productForm.description = '';
    isEditing.value = false;
    editingProductId.value = null;
  };
  </script>