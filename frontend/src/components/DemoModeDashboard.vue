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
  timeout: 500000,
});

export default {
  data: () => ({
    messages: [
      "Welcome to demo mode! Here, \
      you can take a tour and see \
      the key features of the FlorA \
      web application.",
      "This is the dashboard. \
      You can hover or tap on any icon to see \
      the current values for your plant's \
      temperature, humidity, soil moisture, \
      light, or water reservoir status.",
      "Try clicking the SEE MORE button. This \
      will present more details about each plant's \
      status over the past few days.",
      "At the top of the dashboard, alerts will highlight \
      any plants that need attention. You can also see \
      the activity history to the right.",
      "Okay, let's try adding a plant! On the top right \
      of the screen, click the user (this is 'Guest' in \
      demo mode.) Next, click 'Add a Plant'",
    ],
    messageIndex: 0,
  }),
  mounted() {
    this.runDemo();
  },
  methods: {
    runDemo() {
      this.$q.notify({
        type: "demo",
        message: this.messages[this.messageIndex],
        closeBtn: false,
        actions: [
          {
            icon: "mdi-skip-next-outline",
            label: "Next",
            color: "white",
            handler: () => this.updateMessageIndex(),
          },
        ],
      });
    },
    updateMessageIndex() {
      this.messageIndex += 1;
      if (this.messageIndex != this.messages.length) this.runDemo();
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