
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/login', component: () => import('pages/login.vue') },
      { path: '/register', component: () => import('pages/register.vue') },
      {
        path: '/dashboard',
        component: () => import('pages/dashboard.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: '/request-email-confirmation',
        component: () => import('pages/request-email-confirmation.vue'),
        meta: { requiresAuth: true }
      },
      {
        path: '/history',
        component: () => import('pages/history.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: '/add-plants',
        component: () => import('pages/add-plants.vue'),
        meta: { requiresAuth: true },
      },
      {
        path: '/account',
        component: () => import('pages/account.vue'),
        meta: { requiresAuth: true },
      },
    ]
  },
  { // 404 page
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
