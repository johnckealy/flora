<template>
  <q-icon :size="size" :color="clr" :name="ic">
    <q-tooltip  transition-show="scale" transition-hide="scale">
      <span class="text-subtitle2">{{ tp }}</span>
    </q-tooltip>
  </q-icon>
</template>

<script>
export default {
    props: [
        'clr',
        'ic',
        'tp',
        'size'
    ]
};
</script>

<style>
</style>