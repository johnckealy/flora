<template>
  <div>
    <demo-mode-add-plant v-if="demo" :currentTab="tab" />

    <q-tabs v-model="tab" dense class="bg-grey-2 text-teal">
      <q-tab name="step1" icon="mdi-magnify" label="Step 1" />
      <q-tab name="step2" icon="mdi-sprout" label="Step 2" />
      <q-tab name="step3" icon="mdi-check-circle-outline" label="Step 3" />
    </q-tabs>

    <div class="container" style="max-width: 700px">
      <div v-if="tab === 'step1'">
        <h1 class="text-h5 text-center text-weight-bold">
          Step 1/3: <span class="text-weight-regular">Find your plant</span>
        </h1>
        <h6 class="text-subtitle1">
          Let's find out what your plant is so we can give it just the right
          care. If you don't know the specifics, get as close as you can. If you
          have no idea at all, that's OK! Just hit the "No Idea" button below.
        </h6>

        <search-bar
          :stringOptions="stringOptions"
          :plantsIndex="plantsIndex"
          @choice="plantChoice"
        />

        <div class="row">
          <div class="col-12">
            <q-expansion-item
              header-class="text-accent"
              expand-separator
              label="I have no idea!"
              expand-icon-class="hidden"
              dense
            >
              <h6 class="q-mb-none q-mt-md">
                Which of the following would best describe your plant?
              </h6>
              <div class="q-pa-md">
                <q-option-group
                  :options="radioOptions"
                  label="Notifications"
                  type="radio"
                  v-model="radioChoice"
                />
              </div>
            </q-expansion-item>
          </div>
          <div class="col-12 flex justify-end">
            <q-btn
              id="step1-submit"
              class="q-py-none q-px-lg q-mx-lg"
              color="primary"
              @click="tab = 'step2'"
              >Submit</q-btn
            >
          </div>
        </div>
      </div>

      <div v-else-if="tab === 'step2'">
        <h1 class="text-h5 text-center text-weight-bold">
          Step 2/3:
          <span class="text-weight-regular">Name and Place Your Plant</span>
        </h1>
        <h6 class="text-subtitle1">
          Now, give your plant a nickname to keep track of it better, and let us
          know which room it will be in. If you have already purchased your
          FlorA device from us, now is the time to enter the Device ID number.
          If not, that's okay! You can still set up your plant and get basic
          information on how to maintain it yourself.
        </h6>
        <div class="row">
          <div class="col-md-4 col-12 q-pa-sm">
            <q-input
              for="nickname"
              v-model="nickname"
              label="Nickname"
              outlined
              placeholder="Plantly, Spot... Maybe Bob?"
            />
          </div>
          <div class="col-md-4 col-12 q-pa-sm">
            <q-input
              for="room"
              outlined
              v-model="room"
              label="Room"
              placeholder="Sunroom, Hall, etc.."
            />
          </div>
          <div class="col-md-4 col-12 q-pa-sm">
            <q-input
              for="thingspeak-id"
              v-model="thingspeakId"
              outlined
              type="number"
              label="FlorA Device HID#"
              placeholder="ID of your FlorA device"
            />
          </div>
        </div>

        <div class="row q-ma-lg">
          <div class="col-6 q-px-lg">
            <a href="https://floraplantcare.com/" target="_blank">
              <q-btn
                color="negative"
                class="full-width"
                label="Get a FlorA device"
            /></a>
          </div>
          <div class="col-6 q-px-lg">
            <q-btn
              id="step2-submit"
              color="primary"
              class="full-width"
              @click="confirmation"
              label="Submit"
            />
          </div>
        </div>

        <div class="q-py-lg"></div>

        <div class="row items-center q-ma-md">
          <div class="col-3 col-md-2">
            <q-img
              :src="
                plant.large_thumbnail_url
                  ? plant.large_thumbnail_url
                  : require('src/assets/clipart-plant.png')
              "
            />
          </div>
          <div class="col-9 col-md-10 q-pa-md">
            <h6 class="text-h4 roman q-my-sm">
              {{ plant.plant_name }}
            </h6>
            <span class="text-subtitle1 text-grey-9 text-italic q-my-lg">
              {{ plant.scientific_name }}</span
            >
          </div>
        </div>
        <div class="row q-ma-md">
          <div class="roman q-pb-lg text-h6 col-12">
            {{ plant.description }}
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
                {{ plant[feature.field] }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="tab === 'step3'">
        <h1 class="text-h5 text-center text-weight-bold">
          Step 3/3:
          <span class="text-weight-regular">Confirm Your Plant</span>
        </h1>
        <div class="row">
          <div class="col-8">
            <h6 class="text-h4 roman q-my-sm">
              {{ nickname }}
            </h6>
            <span class="text-subtitle1 text-grey-9 text-italic q-my-lg">
              {{ plant.scientific_name }}</span
            >
          </div>
          <div class="col-3">
            <q-uploader
              @uploaded="uploadURL"
              max-file-size="2000000"
              :url="`${apiURL}/upload/`"
              with-credentials
              auto-upload
              :label="`Upload an image of ${nickname}`"
              color="secondary"
              @rejected="onUploadRejected"
            />
          </div>
        </div>
        <div
          v-for="(confirmField, i) in confirmFields"
          :key="i"
          class="row q-my-lg text-subtitle2"
        >
          <div class="col-1 text-grey-8">
            <q-icon size="22px" :name="confirmField.icon" />
          </div>
          <div class="col-3 text-grey-8">
            {{ confirmField.label }}
          </div>
          <div class="col-8 q-pl-lg">
            {{ confirmField.value }}
          </div>
        </div>
        <q-btn id="step3-submit" @click="onSubmit" color="primary">
          {{ settingUp ? "Setting up..." : "Confirm and start tracking!" }}
          <q-spinner-ball class="q-mx-lg" v-if="settingUp" color="white" />
        </q-btn>
        <div>
          <p
            class="q-mt-md text-red"
            v-for="(error, i) in submitErrors"
            :key="i"
          >
            {{ error }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DemoModeAddPlant from "../components/DemoModeAddPlant.vue";
import SearchBar from "../components/SearchBar.vue";

export default {
  data: () => ({
    tab: "step1",
    plant: null,
    radioChoice: null,
    stringOptions: null,
    plantsIndex: null,
    nickname: null,
    room: null,
    thingspeakId: null,
    submitErrors: [],
    uploadHref: null,
    settingUp: false,
    radioOptions: [
      { label: "Generic Tropical Foliage", value: "rec73MHWsvWI3bD9t" },
      { label: "Generic Low Light Plant", value: "recAWxPMILVXSsdrF" },
      { label: "Generic High-Light Plant", value: "recDXQgPw6qjlpJxL" },
      { label: "Generic Succulent", value: "recoQrXzaUVTCAK2S" },
    ],
    fields: [],
    confirmFields: [],
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
  mounted() {
    this.getPlants();
  },
  components: {
    SearchBar,
    DemoModeAddPlant,
  },
  methods: {
    plantChoice(val) {
      this.plant = val;
    },
    uploadURL({ files, xhr }) {
      this.uploadHref = xhr.response.replace(/"/g, "");
    },
    onUploadRejected(rejectedEntries) {
      console.log(rejectedEntries);
      this.$q.notify({
        type: "negative",
        message: `Image uploads must be smaller than 2mb`,
      });
    },
    confirmation() {
      this.confirmFields = [
        {
          label: "Nickname",
          value: this.nickname,
          icon: "mdi-sprout",
        },
        {
          label: "Room",
          value: this.room,
          icon: "mdi-home",
        },
        {
          label: "Device ID#",
          value: this.thingspeakId,
          icon: "mdi-tag-multiple-outline",
        },
      ];
      this.tab = "step3";
      this.submitErrors = [];
    },
    async getPlants() {
      const response = await this.$auth.axios({
        url: "plants_index",
        method: "GET",
      });
      this.plantsIndex = response.data;
      if (this.plantsIndex) {
        this.stringOptions = this.plantsIndex.map((element) => {
          return element.plant_name;
        });
      }
    },
    async onSubmit() {
      if (this.demo) {
        this.$store.commit("setdemo", {});
        this.$q.notify({
          type: "demo",
          message: "That's it for the demo! Registration is free, we hope you'll try it out!",
          timeout: 3000,
        });
        this.$auth.logout();
        this.$router.push('/')
        return;
      }
      this.settingUp = true;
      const postData = {
        nickname: this.nickname,
        room: this.room,
        thingspeak_id: this.thingspeakId,
        airtable_plant_id: this.plant.airtable_id,
        image_url: this.uploadHref,
      };
      try {
        await this.$auth.axios({
          url: "/add_device/",
          data: postData,
          method: "POST",
        });
        this.$q.notify({ message: "Device registered successfully" });
        this.$router.push("/dashboard");
      } catch (e) {
        this.$q.notify({
          message: "There was a problem registering the device",
          color: "red-6",
          icon: "mdi-alert-outline",
        });
        const errors = e.response.data;
        Object.entries(errors).forEach((entry) => {
          if (Array.isArray(entry[1])) {
            if (entry[1][0] === "This field may not be null.") {
              this.submitErrors.push(
                `The ${entry[0]} field may not be left blank. Please give it a value.`
              );
            }
          }
          if (entry[0] === "device_error") {
            this.submitErrors.push(`${entry[1]}`);
          }
        });
      }
      this.settingUp = false;
    },
  },
  computed: {
    apiURL() {
      return process.env.API_URL;
    },
    demo() {
      return this.$store.state.demo;
    },
  },
  watch: {
    radioChoice: function () {
      this.plant = this.radioChoice;
      this.plant = this.plantsIndex.find((el) => {
        return el.airtable_id === this.radioChoice;
      });
    },
  },
};
</script>
