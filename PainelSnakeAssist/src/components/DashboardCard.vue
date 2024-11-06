<template>
    <div 
      class="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 cursor-pointer"
      @click="$emit('click')"
    >
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold text-gray-800">{{ title }}</h2>
        <component :is="iconComponent" class="w-8 h-8 text-indigo-600" />
      </div>
      <p class="text-gray-600">Clique para acessar</p>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  import * as LucideIcons from 'lucide-vue-next';
  
  const props = defineProps({
    title: {
      type: String,
      required: true
    },
    icon: {
      type: String,
      required: true
    }
  });
  
  const iconComponent = computed(() => {
    return LucideIcons[props.icon.charAt(0).toUpperCase() + props.icon.slice(1)];
  });
  </script>