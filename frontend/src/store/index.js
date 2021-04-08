import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

Vue.config.productionTip = false



export default function (/* { ssrContext } */) {
  const Store = new Vuex.Store({
    modules: {},

    state: {
      demo: false
    },
    mutations: {
      setdemo(state, user) {
        if (user.email === 'demo@email.com') {
          state.demo = true;
        }
        else {
          state.demo = false;
        }
      },
    },

    // enable strict mode (adds overhead!)
    strict: process.env.DEBUGGING
  })

  return Store
}
