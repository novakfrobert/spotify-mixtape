import { createApp } from 'vue'
import App from './App.vue'
import { Quasar } from 'quasar'
import quasarUserOptions from './quasar-user-options'
//import type { RouteRecordRaw }  from 'vue-router';

import { createRouter, createWebHashHistory } from 'vue-router'
import Login from './components/Login.vue'
import MixTapeMaker from './components/MixTapeMaker/MixTapeMaker.vue'


const routes = [
    { path: '/', component: Login },

    { path: '/Login', component: Login },
    { path: '/MixtapeMaker', component: MixTapeMaker },
    //{ path: '/about', component: About },
  ]

//   3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: createWebHashHistory(),
    routes: routes, // short for `routes: routes`
  })

createApp(App).use(router).use(Quasar, quasarUserOptions).mount('#app')
