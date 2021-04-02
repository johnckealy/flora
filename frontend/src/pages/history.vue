<template>
  <div class="row justify-center q-pa-lg">
    <div class="col-6">
      <history :limit="30" />
      <q-btn to="/dashboard" class="q-mt-sm" color="primary">Back to dashboard</q-btn>
    </div>
  </div>
</template>

<script>
import History from "../components/History.vue";
export default {
  components: { History },
};
</script>

<style>
</style>