<template>
  <div class="full-height q-pa-sm text-white" :style="style">
    <div class="row">
      <div class="col-12 flex  justify-between">
        <q-icon size="37px" :name="icon" />
        <span class="text-grey-5">{{ date }}</span>
      </div>
      <div class="text-subtitle1 q-pa-md">{{ title }}</div>
    </div>

  </div>
</template>

<script>
export default {
  props: ["title", "icon", "color", "date"],
  computed: {
    style() {
      if (this.color === 'negative') {
        return `background: radial-gradient(circle, #e70000 0%, #5b0000 100%)`;
      }
      else {
        return `background: radial-gradient(circle, #d7a32b 0%, #7a4f00 100%)`;
      }
    }
  },
};
</script>

<style>
</style>