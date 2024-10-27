const routes = [
  {
    path: "/",

    alias: ["/index", "/index.html"],
    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        name: "Index",
        component: () => import("pages/IndexPage.vue"),
      },
    ],
    meta: { transition: "slide-left" },
  },
  {
    path: "/login",

    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        name: "Login",
        component: () => import("pages/LoginPage.vue"),
      },
    ],
    meta: { transition: "slide-left" },
  },

  {
    path: "/update",

    component: () => import("layouts/MainLayout.vue"),
    children: [
      {
        path: "",
        name: "Update",
        component: () => import("pages/UpdateWarningPage.vue"),
      },
    ],
    meta: { transition: "slide-left" },
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
