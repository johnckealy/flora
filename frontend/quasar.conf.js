module.exports = function (/* ctx */) {
  return {
    supportTS: false,

    boot: [
      'auth',
      { path: 'plotly', server: false }
    ],

    css: [
      'app.scss'
    ],

    extras: [
      'roboto-font',
      'mdi-v5'
    ],

    build: {
      vueRouterMode: 'history', // available values: 'hash', 'history'

      env: {
        API_URL: process.env.API_URL
      },
      // transpile: false,
      extendWebpack(cfg) {
      },
    },

    devServer: {
      https: true,
      port: 8080,
      open: false,
      hot: true,
      host: process.env.ORIGIN_URL.replace(/^http(s|):\/\//g, '').replace(/:\d{4}$/g, ''),
      disableHostCheck: true,
    },

    framework: {
      iconSet: 'mdi-v5',
      lang: 'en-us',
      config: {},
      importStrategy: 'auto',

      plugins: ['Notify']
    },

    animations: [],

    ssr: {
      pwa: false
    },

    cordova: {},

    capacitor: {
      hideSplashscreen: true
    },

    electron: {
      bundler: 'packager', // 'packager' or 'builder'

      packager: {},

      builder: {
        appId: 'frontend'
      },

      nodeIntegration: true,

      extendWebpack(/* cfg */) {}
    }
  }
}
