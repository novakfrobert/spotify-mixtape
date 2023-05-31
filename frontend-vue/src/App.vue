<template>
  <div>
    <router-view />
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'LayoutDefault',

  components: {
  },

  setup () {
    return {
      leftDrawerOpen: ref(false)
    }
  }
}
</script>
