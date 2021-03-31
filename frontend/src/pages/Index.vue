<template>
  <div>
    <q-parallax src="~assets/banner.jpg">
      <div class="">
        <div class="row">
          <div class="col-12 text-center q-pa-none flex">
            <h1 class="text-h1 q-ma-none text-white">
              <strong>FlorA</strong>
            </h1>
            <q-img
              width="50px"
              height="50px"
              src="~assets/icon-white.svg"
            ></q-img>
          </div>
        </div>
        <div class="row items-left justify-center">
          <h4 class="text-h4 text-white text-md-left">
            Automated plant care for every plant owner
          </h4>
        </div>
        <div class="row text-center">
          <div class="col-12">
            <q-btn
              color="primary"
              to="/login"
              style="width: 250px; height: 50px"
              class="q-ma-lg text-subtitle1"
            >
              Login
            </q-btn>
            <q-btn
              color="success"
              to="/register"
              style="width: 250px; height: 50px"
              class="q-ma-lg text-subtitle1"
            >
              Get Started
            </q-btn>
          </div>
        </div>
      </div>
    </q-parallax>

    <div class="container" style="max-width: 900px">
      <div class="row q-ma-lg q-pa-lg">
        <div class="col-12  text-center">
          <p class="text-left text-h6 text-italic">
            "We're taking the guesswork out of plants with scientific methods
            and real-world data."
          </p>
          <p class="text-right text-subtitle1">– Nicholas Upton, Founder of FlorA</p>
        </div>
      </div>

      <div class="row q-my-lg">
        <div class="col-12 col-md-6 text-subtitle1" >
          <h2 class="text-h6 q-my-lg">What is FlorA?</h2>
          <p>
            FlorA is a plant automation device. It operates by collecting
            various forms of environmental data, including light, temperature,
            humidity, barometric pressure and soil moisture levels.
          </p>
          <p>
            The device connects to the internet where the readings are
            processed. Based on the local environmental data, the FlorA remote
            server orders the device to water plants, as well as giving care
            advice for that individual plant.
          </p>
        </div>
        <div class="col-12 col-md-6">
          <q-img style="height: 400px; width: 280px"  src="~assets/two-clipart-plants.png"></q-img>
        </div>
      </div>
    </div>
    <q-parallax src="~assets/potted-plants.jpg">
      <div class="row text-subtitle1">
        <div class="col-6  text-white col-md-6 flex-column">
          <div>
            <q-img
              width="200px"
              height="150px"
              class="q-mx-auto"
              src="~assets/gears.svg"
            ></q-img>
            <h4 class="text-center display-1 q-my-5">True Automation</h4>
            <p style="max-width: 500px" class="title text-center">
              FlorA is true houseplant automation. It understands the unique
              needs of each of your plants – providing water and real-time
              environmental monitoring.
            </p>
          </div>
        </div>
        <div
          class="col-12 col-md-6 text-white  flex-column items-center justify-center"
        >
          <div>
            <q-img
              class="q-mx-auto"
              width="130px"
              height="150px"
              src="~assets/traveller.svg"
            ></q-img>
            <h2 class="text-center display-1 q-my-5">Healthy, Happy Plants</h2>
            <p style="max-width: 500px" class="title text-center">
              FlorA’s automation allows busy or traveling plant owners to leave
              even their most sensitive or demanding plants alone for days or
              weeks at a time.
            </p>
          </div>
        </div>
      </div>
    </q-parallax>

    <div class="container">
      <div class="row q-my-lg">
        <div class="col-12 col-md-6 q-pa-lg">
          <q-img style="max-width:300px;" src="~assets/logo.png"></q-img>
        </div>
        <div class="col-12 col-md-6 text-subtitle1 q-pa-lg text-left">
          <h4 class="q-my-lg">How Does it Work?</h4>
          <p>
            FlorA works by connecting your plant to the massive FlorA plant care
            database via your home wireless network. It reads your local
            environment with embedded sensors including area temperature,
            humidity, plant-soil moisture, sunlight and barometric pressure.
          </p>
          <p>
            That information is then securely transmitted to the FlorA server
            where it is analyed against the FlorA database; providing plant
            owners real time statuses and instructions for their individual
            plant.
          </p>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  auth: "guest",
  data: () => ({
    contactEmail: "",
    contactTextBody: "",
  }),
  methods: {},
  computed: {},
};
</script>
