<template>
  <q-card class="dialog-card" style="position: relative">
    <q-btn
      class="q-ma-xs fixed"
      style="z-index: 100"
      size="15px"
      color="dark"
      icon="mdi-close"
      round
      dense
      v-close-popup
    />

    <div v-if="!loading" class="row">
      <div class="col-12 col-md-2">
        <div>
          <q-img
            width="100%"
            style="max-height: 27em"
            :src="
              device.image_url
                ? device.image_url
                : require('src/assets/clipart-plant.png')
            "
          ></q-img>
        </div>
        <div class="q-pa-sm">
          <q-list>
            <q-item
              v-for="(btn, i) in gbtns"
              :key="i"
              clickable
              v-ripple
              class="full-width bg-secondary text-white flex justify-center items-center q-ma-sm"
              :active="link === btn"
              @click="link = btn"
              active-class="bg-blue-8"
            >
              {{ btn }}
            </q-item>
          </q-list>
        </div>
      </div>

      <div class="col-md-5 col-12 q-pa-lg">
        <div class="row">
          <div class="col-12" style="height: 20em">
            <q-no-ssr>
              <plotly-graph :link="link" :dialogData="dialogData" />
            </q-no-ssr>
          </div>
          <div class="col-12 q-pt-lg">
            <div v-for="(item, i) in fields" :key="i">
              <div class="row q-pa-sm items-center">
                <div class="col-2 flex justify-center">
                  <status-icon
                    :size="'25px'"
                    :clr="dialogData.dialog_status[item.field].color"
                    :ic="item.icon"
                    :tp="item.value"
                  />
                </div>
                <div class="col-10 q-px-sm">
                  <span>
                    {{ dialogData.dialog_status[item.field].message }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-5 col-12">
        <div class="row q-ma-md">
          <div class="col-3 col-md-4">
            <q-img src="~assets/plant-backdrop.jpg" height="100%" />
          </div>
          <div class="col-9 col-md-8 q-pa-md">
            <h6 class="text-h4 roman q-my-sm">
              {{ dialogData.nickname }} is a {{ dialogData.plant_name }}
            </h6>
            <span class="text-subtitle1 text-grey-9 text-italic q-my-lg">
              {{ dialogData.scientific_name }}</span
            >
          </div>
        </div>
        <div class="row q-ma-md">
          <div class="roman q-pb-lg text-h6 col-12">
            {{ dialogData.description }}
          </div>
          <div
            v-for="(feature, i) in features"
            :key="i"
            class="col-12 text-subtitle1 q-pa-sm"
          >
            <div class="row text-subtitle2">
              <div class="col-1 text-grey-8">
                <q-icon size="22px" :name="feature.icon" />
              </div>
              <div class="col-3 text-grey-8">
                {{ feature.fieldText }}
              </div>
              <div class="col-8 q-pl-lg">
                {{ dialogData[feature.field] }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="flex full-height justify-center items-center">
      <q-spinner size="10em" />
    </div>
  </q-card>
</template>

<script>
import PlotlyGraph from "./PlotlyGraph.vue";
import StatusIcon from "./StatusIcon.vue";
export default {
  components: { StatusIcon, PlotlyGraph },
  data: () => ({
    dialogData: {},
    loading: false,
    gbtns: ["HUMIDITY (%)", "TEMPERATURE (°F)", "SOIL MOISTURE", "SUN (LUX)"],
    link: "HUMIDITY (%)",
    fields: [],
    features: [
      {
        field: "scientific_name",
        fieldText: "Scientific Name",
        icon: "mdi-scale-balance",
      },
      {
        field: "toxicity",
        fieldText: "Toxicity",
        icon: "mdi-biohazard",
      },
      {
        field: "sun_requirements",
        fieldText: "Sun Requirements",
        icon: "mdi-weather-sunny",
      },
      {
        field: "ideal_soil_type",
        fieldText: "Ideal Soil Type",
        icon: "mdi-wall-sconce-round-variant",
      },
    ],
  }),
  props: ["device"],
  mounted() {
    this.getDialogData();
  },
  methods: {
    async getDialogData() {
      this.loading = true;
      const response = await this.$auth.axios(
        `/dialog_data/${this.device.device_id}`
      );
      this.dialogData = await response.data;

      (this.fields = [
        {
          field: "sun",
          icon: "mdi-white-balance-sunny",
          value: this.dialogData.current_sun
            ? 'Light: ' + this.dialogData.current_sun
            : "Light data not available",
        },
        {
          field: "water",
          icon: "mdi-cup",
          value: this.dialogData.current_waterlevel_ok
            ? "Water is okay"
            : "Water is empty!",
        },
        {
          field: "humidity",
          icon: "mdi-water-percent",
          value: this.dialogData.current_humidity
            ? 'Humidity: ' + this.dialogData.current_humidity + "%"
            : "Humidity data not available",
        },
        {
          field: "temperature",
          icon: "mdi-thermometer-lines",
          value: this.dialogData.current_temp
            ? 'Temperature: ' + this.dialogData.current_temp + " °F"
            : "Temperature data not available",
        },
        {
          field: "soilmoist",
          icon: "mdi-watering-can",
          value: this.dialogData.current_soilmoist
            ? "Soil Moisture: " + this.dialogData.current_soilmoist
            : "Soil Moisture data not available",
        },
      ]),
        (this.loading = false);
    },
  },
};
</script>

<style lang="scss">
.dialog-card {
  width: 85vw;
  max-width: 95vw !important ;
  height: 80vh;
  @media (max-width: $breakpoint-md-max) {
    width: 95vw;
    height: 95vh;
  }
}

.plot-link {
  background-color: red;
}
</style>