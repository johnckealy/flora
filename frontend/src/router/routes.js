
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/Index.vue') },
      { path: '/login', component: () => import('pages/login.vue') },
      { path: '/register', component: () => import('pages/register.vue') },
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
    ]
  },
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '/dashboard',
        component: () => import('pages/dashboard.vue'),
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
