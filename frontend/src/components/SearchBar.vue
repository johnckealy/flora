<template>
  <div class="q-pa-md">
    <div class="q-gutter-md row">
      <q-select
        outlined
        rounded
        :value="model"
        use-input
        hide-selected
        fill-input
        input-debounce="0"
        :options="options"
        @filter="filterFn"
        @input-value="setModel"
        placeholder="Search the FlorA database..."
        class="full-width"
      >
        <template v-slot:prepend>
          <q-icon class="q-pl-sm" name="mdi-magnify" />
        </template>
      </q-select>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      model: null,
      options: null,
    };
  },
  props: ["plantsIndex", "stringOptions"],
  methods: {
    filterFn(val, update, abort) {
      update(() => {
        const needle = val.toLocaleLowerCase();
        this.options = this.stringOptions.filter(
          (v) => v.toLocaleLowerCase().indexOf(needle) > -1
        );
      });
    },
    setModel(val) {
      this.model = val;
    },
  },

  watch: {
    model: function () {
      const choice = this.plantsIndex.find((el) => {
        return el.plant_name === this.model;
      });
      this.$emit("choice", choice);
    },
  },
};
</script>

<style>
</style>