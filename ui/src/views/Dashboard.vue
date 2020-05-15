<template>
  <div class="dashboard">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Dashboard"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld
  }
}
</script>
