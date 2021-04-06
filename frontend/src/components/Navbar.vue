<template>
  <q-toolbar class="bg-secondary">
    <router-link :to="authUser ? '/dashboard' : '/'">
      <div>
        <img alt="logo" src="~assets/icon-white.svg" width="50px" />
      </div>
    </router-link>

    <q-space />

    <q-btn
      v-if="!authUser"
      to="/login"
      icon="mdi-account"
      class="q-ma-md"
      no-caps
      flat
      dense
    >
      <span class="text-h6 q-mx-sm">Login</span>
    </q-btn>

    <div v-else class="q-pa-md">
      <q-btn-dropdown
        icon="mdi-account"
        flat
        :label="authUser ? authUser.first_name : ''"
      >
        <q-list>
          <q-item clickable v-close-popup @click="$router.push('/dashboard')">
            <q-item-section>
              <q-item-label>Dashboard</q-item-label>
            </q-item-section>
          </q-item>

          <q-item clickable v-close-popup @click="$router.push('/add-plants')">
            <q-item-section>
              <q-item-label>Add a plant</q-item-label>
            </q-item-section>
          </q-item>

          <q-item clickable v-close-popup @click="$router.push('/account')">
            <q-item-section>
              <q-item-label>Account</q-item-label>
            </q-item-section>
          </q-item>

          <q-item clickable v-close-popup @click="logout">
            <q-item-section>
              <q-item-label>Logout</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
    </div>
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
    authUser() {
      return this.$auth.user();
    },
  },
};
</script>

<style>
</style>