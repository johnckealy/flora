<template>
  <q-layout view="lHh Lpr lFf">
    <!-- Navigation bar -->
    <q-header elevated>
      <navbar />
    </q-header>

    <!-- Main content Body -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import Navbar from "components/Navbar.vue";

export default {
  name: "MainLayout",
  components: {
    Navbar,
  },
  mounted() {
    this.$q.notify.setDefaults({
      color: "green-4",
      textColor: "white",
      icon: "mdi-cloud-check",
      message: "Successful",
      position: "bottom-right",
      timeout: 2000,
      actions: [{ icon: "mdi-close", color: "white" }],
    });
  },
};
</script>
