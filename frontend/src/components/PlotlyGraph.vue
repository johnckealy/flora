<template>
  <div style="height: 100%; width: 100%">
    <vue-plotly
      v-if="dialogData"
      style="height: 100%; width: 100%"
      :layout="layout"
      :data="plotData"
      :display-mode-bar="false"
    ></vue-plotly>
  </div>
</template>

<script>
export default {
  data: () => ({
    layout: {
      margin: {
        l: 30,
        r: 30,
        b: 25,
        t: 30,
        pad: 5,
      },
      title: false,
    },
    plotData: [
      {
        x: [],
        y: [],
        type: "scatter",
      },
    ],
  }),
  mounted() {
    this.showPlot();
  },
  props: ["dialogData", "link"],
  watch: {
    link: function ()  {
      this.showPlot()
    },
  },
  methods: {
    showPlot() {
      this.getYData()
      this.soilMoistInfo = false;
      this.plotData = [
        {
          x: this.dialogData.datetime_history,
          y: this.yData,
        },
      ];
    },
    getYData() {
      if (this.link == "HUMIDITY (%)") {
        this.yData = this.dialogData.humidity_history;
      } else if (this.link == "TEMPERATURE (°F)") {
         this.yData = this.dialogData.temperature_history;
      } else if (this.link == "SOIL MOISTURE") {
        this.yData = this.dialogData.soilmoist_history;
      } else if (this.link == "SUN (LUX)") {
        this.yData = this.dialogData.sun_history;
      } else {
        throw "There is no field selected for the graph";
      }
    },
  },
};
</script>

<style>
</style>