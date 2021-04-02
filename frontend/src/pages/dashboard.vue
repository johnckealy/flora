<template>
  <q-page class="flex column flex-center">
    <q-img src="~assets//plant-backdrop.jpg" height="150vh">
      <div class="absolute-full">
        <div class="container">
          <div class="row">
            <div class="desktop-only col-md-4 q-ma-lg col-10">
              <q-card flat bordered>
                <q-card-section class="q-pa-lg text-black">
                  <h6 class="text-subtitle1 q-ma-none text-weight-regular">
                    Hi {{ authUserName }}, <br />
                    Let's see how your plants are doing. You can see your alerts
                    to the right and dig into the data below.
                  </h6>
                </q-card-section>
              </q-card>
            </div>

            <div class="col-12 col-md-6"></div>
          </div>
          <div class="row">
            <div class="col-md-9">
              <div v-for="(device, i) in dash_data" :key="i">
                <q-card class="q-my-sm text-black">
                  <div class="row items-center justify-center">
                    <div class="q-px-sm col-3 col-md-1">
                      <q-img
                        width="60px"
                        height="60px"
                        :src="device.small_thumbnail_url"
                      ></q-img>
                    </div>
                    <div class="q-pa-sm col-md-2 col-9">
                      <h6 class="q-ma-none q-ml-sm">{{ device.nickname }}</h6>
                      <em class="text-grey-8 q-ml-sm">
                        {{ device.scientific_name }}</em
                      >
                    </div>
                    <div
                      class="row justify-center items-center q-pt-md col-md-6"
                    >
                      <div class="row" style="width: 100%">
                        <div class="col-12 col-md-12 flex-around">
                          <status-icon
                            :clr="device.status.water.color"
                            :ic="'mdi-cup'"
                            :size="'40px'"
                            :tp="`Water ${
                              device.current_waterlevel_ok
                                ? 'is okay'
                                : 'is empty!'
                            }`"
                          />
                          <status-icon
                            :clr="device.status.sun.color"
                            :size="'40px'"
                            :ic="'mdi-white-balance-sunny'"
                            :tp="`Light (${device.current_sun})`"
                          />
                          <status-icon
                            :clr="device.status.humidity.color"
                            :size="'40px'"
                            :ic="'mdi-water-percent'"
                            :tp="`Humidity (${device.current_humidity}%)`"
                          />
                          <status-icon
                            :clr="device.status.temperature.color"
                            :size="'40px'"
                            :ic="'mdi-thermometer-lines'"
                            :tp="`Soil Moisture (${device.current_temp} °F)`"
                          />
                          <status-icon
                            :clr="device.status.soilmoist.color"
                            :size="'40px'"
                            :ic="'mdi-watering-can'"
                            :tp="`Soil Moisture (${device.current_soilmoist})`"
                          />
                        </div>
                      </div>
                      <div class="q-pa-md col-12 col-md-12">
                        {{ device.status.dashboard_message }}
                      </div>
                    </div>
                    <div class="col-12 col-md-3 q-px-sm text-grey-8">
                      <div class="row q-pa-none">
                        <div class="col-6 text-right q-pa-sm col-md-12">
                          {{ device.room }} – {{ device.device_id }}
                        </div>
                        <div class="col-6 col-md-12 q-py-sm">
                          <q-btn @click="openDialog(device)" color="accent"
                            >See More</q-btn
                          >
                         <q-dialog v-model="dialog" >
                           <Dialog :device="dialogData" />
                         </q-dialog>
                          <q-btn
                            color="black"
                            icon="mdi-trash-can-outline"
                            flat
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </q-card>
              </div>
            </div>
            <div class="col-md-3 q-pa-lg">
              <history :limit="3" />
              <q-btn to="/history" class="full-width q-mt-sm" color="primary"
                >See full history</q-btn
              >
            </div>
          </div>
        </div>
      </div>
    </q-img>
  </q-page>
</template>

<script>
import Dialog from '../components/Dialog.vue';
import History from "../components/History.vue";
import StatusIcon from "../components/StatusIcon.vue";
export default {
  data: () => ({
    dash_data: null,
    alerts: [],
    dialog: false,
    dialogData: null
  }),
  components: {
    StatusIcon,
    History,
    Dialog,
  },
  mounted() {
    this.getDashboardData();
  },
  methods: {
    async getDashboardData() {
      try {
        const resp = await this.$auth.axios.get("/dashboard_data/");
        this.dash_data = resp.data;
      } catch {
        console.log("Couldnt retrieve dashboard data. Are you logged in?");
      }
      this.dash_data.forEach((device) => {
        this.alerts = [...this.alerts, ...device.status.alerts];
      });
      this.alerts = this.alerts.slice(0, 4);
    },
    openDialog(device) {
      this.dialogData = device;
      this.dialog = true;
    },
  },
  computed: {
    authUserName() {
      const user = this.$auth.user();
      if (user) {
        return user.first_name;
      }
    },
  },
};
</script>


<style lang="scss">
</style>