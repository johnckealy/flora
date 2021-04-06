<template>
  <div class="container">

    <div class="row q-pa-lg q-ma-lg">
      <div class="col-12 items-center justify-center flex">
        <q-img style="max-width: 300px" src="~assets/logo.png"></q-img>
      </div>
      <div class="col-12 items-center justify-center flex">
        <h1 class="text-h4">Account settings</h1>
      </div>
    </div>
    <div class="row justify-center">
      <div class="col-md-6 col-12">
        <q-form @submit.prevent="onSubmit" class="q-gutter-md">
          <div class="row items-center">
            <div class="col-md-5 col-12">
              <span class="text-subtitle1 q-px-lg">Email Address</span>
            </div>
            <div class="col-md-7 q-pb-lg col-12">
              <q-input disable class="q-pa-none" v-model="email" outlined />
            </div>

            <div class="col-md-5 col-12">
              <span class="text-subtitle1 q-px-lg">First Name</span>
            </div>
            <div class="col-md-7 q-pb-lg col-12">
              <q-input
                class="q-pa-none"
                v-model="firstName"
                lazy-rules="ondemand"
                :rules="[
                  (val) =>
                    (val && val.length > 0) || 'Please provide your name',
                ]"
                outlined
              >
                <q-btn
                  class="q-ma-sm full-width q-py-xs q-mx-auto"
                  type="submit"
                  no-caps
                  icon="mdi-update"
                  flat
                  color="accent"
                  >{{ loading ? "Updating..." : "Update" }}
                  <q-spinner-ball class="" v-if="loading" color="white" />
                </q-btn>
              </q-input>
            </div>
          </div>
        </q-form>
        <q-form @submit.prevent="passwordChange" class="q-gutter-md">
          <div class="row items-center">
            <div class="col-md-6 col-12">
              <span class="text-subtitle1 q-px-lg">Password</span>
            </div>
            <div class="col-md-6 col-12">
              <q-expansion-item
                expand-separator
                icon="mdi-lock-reset"
                label="Update Password"
                header-class="text-white bg-secondary"
              >
                <div>
                  <q-input
                    class="q-mt-sm"
                    label="New Password"
                    v-model="new_password1"
                    outlined
                    type="password"
                    lazy-rules="ondemand"
                    :rules="[
                      (val) =>
                        (val && val.length > 0) || 'Please provide a value',
                    ]"
                  />
                  <q-input
                    class="q-mb-xs"
                    label="Confirm New Password"
                    v-model="new_password2"
                    outlined
                    type="password"
                    lazy-rules="ondemand"
                    :rules="[
                      (val) =>
                        (val && val.length > 0) || 'Please provide a value',
                    ]"
                  />
                </div>
                <q-btn
                  class="q-ma-sm full-width q-py-xs q-mx-auto"
                  type="submit"
                  color="primary"
                  >{{ loading ? "Resetting PW..." : "Submit" }}
                  <q-spinner-ball class="" v-if="loading" color="white" />
                </q-btn>
              </q-expansion-item>
            </div>
          </div>
        </q-form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    email: "",
    firstName: "",
    new_password1: null,
    new_password2: null,
    fullscreen: false,
  }),
  created() {
    this.loadAccountDetails();
  },
  methods: {
    async loadAccountDetails() {
      try {
        const details = await this.$auth.axios({
          url: "/user/",
          method: "GET",
        });
        this.email = details.data.email;
        this.firstName = details.data.first_name;
      } catch {
        this.$q.notify({
          message: "There was a problem obtaining your details",
          color: "red-6",
          icon: "mdi-alert-outline",
        });
      }
    },
    async onSubmit() {
      try {
        const details = await this.$auth.axios({
          url: "/user/",
          data: {
            first_name: this.firstName,
          },
          method: "PATCH",
        });
        this.$q.notify({ message: "Successfully updated user details" });
      } catch {
        this.$q.notify({
          message: "There was a problem updating your details",
          color: "red-6",
          icon: "mdi-alert-outline",
        });
      }
    },
    async passwordChange() {
      try {
        const details = await this.$auth.axios({
          url: "/password/change/",
          data: {
            new_password1: this.new_password1,
            new_password2: this.new_password2,
          },
          method: "POST",
        });
        this.$q.notify({ message: "Successfully updated user password" });
      } catch {
        this.$q.notify({
          message: "There was a problem updating your password",
          color: "red-6",
          icon: "mdi-alert-outline",
        });
      }
    },
  },
};
</script>

<style>
</style>