<template>
  <q-page class="flex column flex-center">
    <q-img src="~assets//plant-backdrop.jpg" height="150vh">
      <div class="absolute-full" style="overflow: auto">
        <div class="container">
          <div class="row">
            <div class="desktop-only col-md-4 q-ma-lg col-10">
              <q-card flat bordered>
                <q-card-section class="q-pa-lg text-black">
                  <h6 class="text-subtitle2 q-ma-none text-weight-regular">
                    Hi {{ authUserName }}, <br />
                    Let's see how your plants are doing. You can see your alerts
                    to the right and dig into the data below.
                  </h6>
                </q-card-section>
              </q-card>
            </div>
            <div v-if="alerts[0]" class="col-md-4 col-12">
              <q-carousel
                height="150px"
                swipeable
                animated
                :autoplay="6000"
                transition-next="slide-left"
                transition-prev="slide-right"
                v-model="slide"
                infinite
                style="box-shadow: #2e382e 1px 1px 12px 1px"
              >
                <q-carousel-slide
                  v-for="(alert, index) in alerts"
                  :key="index"
                  class="q-pa-none"
                  :name="index"
                >
                  <alert-card
                    :color="alert.color"
                    :title="alert.message"
                    :icon="alert.icon"
                    :date="alert.date"
                  />
                </q-carousel-slide>
              </q-carousel>
            </div>
          </div>
          <div class="row">
            <div class="col-md-9">
              <div>
                <q-card
                  v-if="dash_data.length === 0"
                  class="q-my-sm q-pa-lg text-black items-center flex justify-center"
                >
                  <h6 class="q-ma-none text-weight-regular">
                    You currently have no devices set up. Add a device to get
                    started!
                  </h6>
                  <q-btn to="/add-plants" color="dark" class="q-mx-lg"
                    >Add a Device</q-btn
                  >
                </q-card>
              </div>
              <div v-for="device in dash_data" :key="device.device_id">
                <q-card class="q-my-sm text-black">
                  <div class="row items-center justify-center">
                    <div class="q-px-sm col-3 col-md-1">
                      <q-img
                       width="60px" height="60px"
                        :src="
                          device.image_url
                            ? device.image_url
                            : require('src/assets/clipart-plant.png')
                        "
                      />
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
                            :tp="`Light ${
                              device.current_sun
                                ? device.current_sun
                                : ' data is not available'
                            }`"
                          />
                          <status-icon
                            :clr="device.status.humidity.color"
                            :size="'40px'"
                            :ic="'mdi-water-percent'"
                            :tp="`Humidity ${
                              device.current_humidity
                                ? `${device.current_humidity} %`
                                : ' data is not available'
                            }`"
                          />
                          <status-icon
                            :clr="device.status.temperature.color"
                            :size="'40px'"
                            :ic="'mdi-thermometer-lines'"
                            :tp="`Temperature ${
                              device.current_temp
                                ? `${device.current_temp} °F`
                                : ' data is not available'
                            }`"
                          />
                          <status-icon
                            :clr="device.status.soilmoist.color"
                            :size="'40px'"
                            :ic="'mdi-watering-can'"
                            :tp="`Soil Moisture ${
                              device.current_soilmoist
                                ? device.current_soilmoist
                                : ' data is not available'
                            }`"
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
                          {{ device.room }} – {{ device.thingspeak_id }}
                        </div>
                        <div class="col-6 col-md-12 q-py-sm">
                          <q-btn @click="openDialog(device)" color="accent"
                            >See More</q-btn
                          >
                          <q-dialog v-model="dialog">
                            <Dialog :device="dialogData" />
                          </q-dialog>
                          <q-btn
                            color="black"
                            rounded
                            icon="mdi-trash-can-outline"
                            flat
                            @click="deleteDialog(device)"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </q-card>
              </div>
            </div>
            <q-dialog v-model="confirmDeleteDialog" persistent>
              <q-card>
                <q-card-section class="row items-center">
                  <q-avatar
                    icon="mdi-sprout"
                    color="secondary"
                    text-color="white"
                  />

                  <span v-if="deviceForDeletion" class="q-ma-lg"
                    >Are you sure you'd like to delete
                    <strong>{{ deviceForDeletion.nickname }}</strong> ?
                  </span>
                </q-card-section>

                <q-card-actions align="right">
                  <q-btn flat label="Cancel" color="accent" v-close-popup />
                  <q-btn
                    @click="onDeleteDevice"
                    flat
                    label="Confirm"
                    color="primary"
                    v-close-popup
                  />
                </q-card-actions>
              </q-card>
            </q-dialog>
            <div class="desktop-only col-md-3 q-pa-lg">
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
import AlertCard from "../components/AlertCard.vue";
import Dialog from "../components/Dialog.vue";
import History from "../components/History.vue";
import StatusIcon from "../components/StatusIcon.vue";
export default {
  data: () => ({
    dash_data: [],
    alerts: [],
    dialog: false,
    dialogData: null,
    confirmDeleteDialog: false,
    deviceForDeletion: null,
    slide: 1,
  }),
  components: {
    StatusIcon,
    History,
    Dialog,
    AlertCard,
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
    deleteDialog(device) {
      this.confirmDeleteDialog = true;
      this.deviceForDeletion = device;
    },
    onDeleteDevice() {
      try {
        this.$auth.axios({
          url: `/delete_device/${this.deviceForDeletion.device_id}`,
          method: "DELETE",
        });
        this.$q.notify({
          message: `${this.deviceForDeletion.nickname} was deleted successfully.`,
        });
        this.dash_data = this.dash_data.filter((device) => {
          return device.device_id != this.deviceForDeletion.device_id;
        });
      } catch {
        this.$q.notify({
          message: "There was an issue deleting the device",
          color: "red-6",
          icon: "mdi-alert-outline",
        });
      }
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