<template>
  <q-toolbar class="bg-secondary">
    <router-link to="/">
      <div @click="$router.push('/')">
        <img alt="logo" src="~assets/icon-white.svg" width="50px" />
      </div>
    </router-link>

    <span class="text-h6 q-mx-sm">{{ authUser ? authUser.first_name : "" }}</span>
    <q-space />

    <q-btn to="/add-plants" color="dark">Add a Plant</q-btn>

    <q-btn v-if="!authUser" to="/login" icon="mdi-account" class="q-ma-md" no-caps flat dense>
      <span class="text-h6 q-mx-sm">Login</span>
    </q-btn>
    <q-btn v-else @click="logout" icon="mdi-logout" class="q-ma-md" no-caps flat dense
      ><span class="text-h6 q-mx-sm">Logout</span>
    </q-btn>
  </q-toolbar>
</template>

<script>
export default {
  name: "Navbar",

  methods: {
    async logout() {
      try {
        await this.$auth.logout();
        this.$q.notify({ message: "Successfully logged out" });
        this.$router.push("/");
      } catch {
        this.$q.notify({
          message: "There was a problem logging out.",
          color: "red-6",
          icon: "mdi-alert-outline",
        });
      }
    },
  },
  computed: {
    async authUser() {
      return await this.$auth.user();
    },
  },
};
</script>

<style>
</style>