<template>
  <div class="container">
    <div class="row items-center">
      <div class="col-8"><h4>Create a FlorA account</h4></div>
      <div class="col-4">
        <q-img width="100%" src="~assets/logo.png"></q-img>
      </div>
    </div>

    <h6 class="text-weight-regular">
      The easiest way to get started with FlorA is to create a free account and
      look around :)
    </h6>

    <q-form @submit="onSubmit" class="q-gutter-md">
      <q-input
        v-model="firstName"
        label="First Name"
        lazy-rules="ondemand"
        :rules="[
          (val) => (val && val.length > 0) || 'Please provide a first name',
        ]"
        outlined
      />
      <q-input
        v-model="email"
        label="Email address"
        lazy-rules="ondemand"
        :rules="[
          (val) => (val && val.length > 0) || 'Please provide an email address',
        ]"
        outlined
      />

      <q-input
        v-model="password1"
        label="Choose a password"
        type="password"
        lazy-rules="ondemand"
        :rules="[
          (val) => (val && val.length > 0) || 'Please provide a password',
        ]"
        outlined
      />

      <q-input
        v-model="password2"
        label="Repeat password"
        type="password"
        lazy-rules="ondemand"
        :rules="[
          (val) => (val && val.length > 0) || 'Please provide a password',
        ]"
        outlined
      />

      <div v-if="errorMessages" class="text-body1 text-red">
        <p v-for="(message, i) in errorMessages" :key="i">
          <q-icon color="red" size="18px" name="mdi-alert-outline-outline" />
          {{ message }}
        </p>
      </div>

      <div>
        <q-btn
          no-caps
          glossy
          class="q-ml-md full-width q-mx-auto"
          type="submit"
          color="primary"
          >{{ loading ? "Registering..." : "Sign Up" }}
          <q-spinner-ball class="q-mx-lg" v-if="loading" color="white" />
        </q-btn>
      </div>
    </q-form>

    <div class="text-subtitle1 q-pa-lg q-ma-md"
      >Already have an account? <a href="/login">Sign In</a>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: null,
      email: null,
      firstName: null,
      password1: null,
      password2: null,
      errorMessages: "",
      loading: false,
    };
  },
  methods: {
    async onSubmit() {
      this.loading = true;
      const resp = await this.$auth.register({
        username: this.email,
        email: this.email,
        first_name: this.firstName,
        password1: this.password1,
        password2: this.password2,
      });
      if (resp.status == 201) {
        this.$q.notify({ message: "Account created successfully" });
        this.$router.push("/request-email-confirmation");
      } else {
        this.$q.notify({
          message: "Registration failed!",
          color: "red-6",
          icon: "mdi-alert-outline",
        });
        this.errorMessages = resp;
      }
      this.loading = false;
    },
  },
};
</script>