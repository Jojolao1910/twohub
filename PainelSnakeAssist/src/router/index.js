import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

import Login from "@/components/Login.vue";
import DashboardView from "@/components/DashboardView.vue";
import ProductManagement from "@/components/ProductManagement.vue";
import ProductList from "@/components/ProductList.vue";
import OrderList from "@/components/OrderList.vue";
import SupportDashboard from "@/components/SupportDashboard.vue";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: "/produtos/gerenciar",
    name: "ProductManagement",
    component: ProductManagement,
    meta: { requiresAuth: true },
  },
  {
    path: "/produtos/lista",
    name: "ProductList",
    component: ProductList,
    meta: { requiresAuth: true },
  },
  {
    path: "/pedidos/andamento",
    name: "OrderList",
    component: OrderList,
    meta: { requiresAuth: true },
  },
  {
    path: "/atendimento",
    name: "SupportDashboard",
    component: SupportDashboard,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  console.log(
    `Navigating to ${to.path}, Authenticated: ${authStore.isAuthenticated}`
  );

  if (
    to.matched.some((record) => record.meta.requiresAuth) &&
    !authStore.isAuthenticated
  ) {
    next("/login");
  } else {
    next();
  }
});

export default router;
