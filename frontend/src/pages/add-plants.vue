<template>
  <div>
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
              <h6 class="q-mb-none q-mt-md">Which of the following would best describe your plant?</h6>
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
              class="q-py-none q-px-lg q-mx-lg"
              color="primary"
              @click="tab = 'step2'"
              >Submit</q-btn
            >
          </div>
        </div>
      </div>

      <div v-if="tab === 'step2'">

          <h2>You chose the  {{ plant.plant_name }}</h2>
          <p>To be continued...</p>
      </div>




    </div>
  </div>
</template>

<script>
import SearchBar from "../components/SearchBar.vue";

export default {
  data: () => ({
    tab: "step1",
    plant: null,
    radioChoice: null,
    stringOptions: null,
    plantsIndex: null,
    radioOptions: [
      { label: "Generic Tropical Foliage", value: "rec73MHWsvWI3bD9t" },
      { label: "Generic Low Light Plant", value: "recAWxPMILVXSsdrF" },
      { label: "Generic High-Light Plant", value: "recDXQgPw6qjlpJxL" },
      { label: "Generic Succulent", value: "recoQrXzaUVTCAK2S" },
    ],
  }),
  mounted() {
    this.getPlants();
  },
  components: {
    SearchBar,
  },
  methods: {
    plantChoice(val) {
      this.plant = val;
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
