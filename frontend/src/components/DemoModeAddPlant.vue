<template></template>

<script>
import { Notify } from "quasar";
Notify.registerType("demo", {
  color: "teal-8",
  classes: "demo-message",
  multiLine: true,
  icon: "mdi-play-box-outline",
  position: "top-left",
  closeBtn: false,
  timeout: 60000,
});

export default {
  data: () => ({
    notification: null,
    message1:
      "Let's add a plant! <hr/> Ideally, you'll have already purchased a FlorA \
      device from us when setting up. First, use the  \
      search bar to find your plant's species. ",
    message2:
      "This screen is where you would give your plant a \
      nickname and other details.",
    message3:
      "And finally, you can add an optional image of your \
      plant, and confirm the details.",
  }),
  mounted() {
    this.runDemo();
  },
  props: ["currentTab"],
  methods: {
    runDemo() {
      if (this.currentTab === "step1") {
        this.notification = this.$q.notify({
          type: "demo",
          html: true,
           timeout: 0,
          message: this.message1,
          closeBtn: false,
        });
      }
    },
  },
  watch: {
    currentTab: function () {
      if (this.currentTab === "step2") {
        this.notification()
        this.notification = this.$q.notify({
          type: "demo",
          message: this.message2,
          closeBtn: false,
        });
      } else if (this.currentTab === "step3") {
        this.notification()
        this.$q.notify({
          type: "demo",
          message: this.message3,
          closeBtn: false,
          timeout: 5000,
        });
      }
    },
  },
};
</script>


<style lang="scss">
.demo-message {
  max-width: 400px;
  font-size: 17px;
}
</style>