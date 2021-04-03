<template>
  <div class="container">
    <q-img style="max-width: 300px" src="~assets/logo.png"></q-img>

    <div style="padding: 35px 0"></div>

    <q-form @submit="onSubmit" class="q-gutter-md">
      <q-input
        v-model="username"
        label="Email"
        lazy-rules="ondemand"
        :rules="[
          (val) => (val && val.length > 0) || 'Please provide your email',
        ]"
        outlined
      />

      <q-input
        v-model="password"
        label="Password"
        type="password"
        lazy-rules="ondemand"
        :rules="[
          (val) => (val && val.length > 0) || 'Please provide your password',
        ]"
        outlined
      />

      <div v-if="errorMessages" class="text-body1 text-red">
        <p v-for="(message, i) in errorMessages" :key="i">
          <q-icon color="red" size="18px" name="mdi-alert-outline" />
          {{ message }}
        </p>
      </div>

      <div>
        <q-btn
          class="q-ml-md full-width q-py-xs q-mx-auto"
          type="submit"
          color="primary"
          >{{ loading ? "Signing in..." : "Sign in" }}
          <q-spinner-ball class="q-mx-lg" v-if="loading" color="white" />
        </q-btn>
      </div>
    </q-form>

    <div class="row">
      <div class="col-12 q-my-xs flex justify-center">
        <router-link to="/register" class="text-primary">Forgot password?</router-link>
      </div>
    </div>

    <div class="text-subtitle1 q-pa-md q-ma-md">
      Don't have an account? Register <a href="/register">here.</a>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: null,
      password: null,
      loginErrorMessage: false,
      errorMessages: [],
      loading: false,
    };
  },
  methods: {
    async onSubmit() {
      this.loading = true;
      const response = await this.$auth.login({
        username: this.username,
        password: this.password,
      });
      if (response.status === 200) {
        this.$q.notify({ message: "Login was successful" });
        this.$router.push(this.$auth.redirectUrl());
      } else {
        this.$q.notify({
          message: "Login failed!",
          color: "red-6",
          icon: "mdi-alert-outline",
        });
        this.errorMessages = response;
      }
      this.loading = false;
    },
  },
};
</script>