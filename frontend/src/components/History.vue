<template>
  <div class="row justify-center ">
    <div class="col-6" style="width: 100%">
      <q-card flat bordered class="history-card q-pa-sm">
        <q-card-section>
          <div class="text-black text-h5 text-center"><strong>History</strong></div>
        </q-card-section>

        <div v-for="(entry, i) in history" :key="i" class="text-black q-pa-md">
          <q-card-section class="q-py-none text-grey-8">
            {{ entry.date }}
          </q-card-section>
          <q-card-section class="q-py-sm">
            {{ entry.message }}
          </q-card-section>
          <q-separator inset />
        </div>
      </q-card>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    history: [{ date: null, message: null }],
  }),
  props: ["limit"],
  mounted() {
    this.getHistory();
  },
  methods: {
    async getHistory() {
      try {
        const resp = await this.$auth.axios.get(
          `/history/?limit=${this.limit}`
        );
        this.history = resp.data;
      } catch {
        console.log("Couldnt retrieve history data.");
      }
    },
  },
};
</script>

<style>
.history-card {
  max-width: 600px;
}
</style>