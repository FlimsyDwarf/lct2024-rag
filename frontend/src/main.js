import Vue from 'vue';
import App from './App.vue';
import Vuetify from 'vuetify/lib';
import 'vuetify/dist/vuetify.min.css';
import './assets/css/style.css';


Vue.config.productionTip = false;

Vue.use(Vuetify);

const vuetify = new Vuetify({
  theme: {
    themes: {
      dark: {
        primary: '#5E35B1',
        secondary: '#F0E6FE',
        accent: '#7E57C2',
        error: '#E53935',
        info: '#1E88E5',
        success: '#43A047',
        warning: '#FB8C00',
      },
    },
    dark: true,
  },
});

new Vue({
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
