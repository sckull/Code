<template>
  <div id="app">
    <v-app>
      <Pokemon/>
    </v-app>
  </div>
</template>

<script>
import Pokemon from './components/Pokemon.vue'
export default {
  components: { Pokemon },
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
