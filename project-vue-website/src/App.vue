<template>
  <div id="app">
    <h1>Is my room too cold?</h1>
    <img alt="Vue logo" src="./assets/logo.png">
    <HelloWorld msg="kek"/>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  }
}
</script>

<style>
body {
  margin: 0;
  width: 100%;
  height: 100%;
  background-image: linear-gradient(135deg, #78d8aa 0%,#50b1ed 52%,#4f68e9 100%); /* Standard syntax (must be last) */
  background-repeat: no-repeat;
  background-attachment: fixed;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
