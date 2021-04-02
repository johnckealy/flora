<template>
  <q-card class="dialog-card">
    <!-- <div class="flex items-start"> -->
    <!-- <q-space /> -->
    <!-- <q-btn size="25px" icon="mdi-close" flat round dense v-close-popup /> -->
    <!-- </div> -->

    <div v-if="!loading" class="row">
      <div class="col-12 col-md-3">
        <div>
          <q-img
            width="100%"
            style="max-height: 27em"
            :src="
              device.small_thumbnail_url
                ? device.small_thumbnail_url
                : require('src/assets/no-plant.svg')
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

      <div class="col-md-5 q-pa-lg">

        <div>PLOTLY</div>

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
      
      <div class="col-md-4">
        <div>PLANT</div>
      </div>
    </div>

    <div v-if="loading" class="flex full-height justify-center items-center">
      <q-spinner size="10em" />
    </div>
  </q-card>
</template>

<script>
import StatusIcon from "./StatusIcon.vue";
export default {
  components: { StatusIcon },
  data: () => ({
    dialogData: {},
    loading: false,
    gbtns: ["HUMIDITY (%)", "TEMPERATURE (°F)", "SOIL MOISTURE", "SUN (LUX)"],
    link: "HUMIDITY (%)",
    fields: [],
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
          value: `${this.dialogData.current_sun}`,
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
          value: this.dialogData.current_humidity + " %",
        },
        {
          field: "temperature",
          icon: "mdi-thermometer-lines",
          value: this.dialogData.current_temp + " °F",
        },
        {
          field: "soilmoist",
          icon: "mdi-watering-can",
          value: this.dialogData.current_soilmoist,
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