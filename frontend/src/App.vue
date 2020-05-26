<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png">
    <Chart/>
    <img alt="Vue logo" src="./assets/logo.png">
    <Map/>
  </div>
</template>

<script>
import Chart from './components/Chart.vue'
import Map from './components/Map.vue'

export default {
  name: 'App',
  components: {
    Chart,
    Map
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
