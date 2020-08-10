<template>
  <div class="hello">
    <h1>Most Recent Reads</h1>
    <h3>Sensors are read once per minute, Both sensors currently inside.</h3>
    <div class="card card-1">
    <h1>Inside</h1>
    <div v-if="timestamp">
      <p>Timestamp: {{timestamp}}</p>
    </div>
    <div v-if="insideTemp">
      <p>Temperature: {{Number((insideTemp).toFixed(1))}}°C</p>
    </div>
    <div v-if="insideHum">
      <p>Humidity: {{Number((insideHum).toFixed(1))}}%</p>
    </div>
    </div>
    <div class="card card-1">
    <h1>Outside</h1>
    <div v-if="timestamp">
      <p>Timestamp: {{timestamp}}</p>
    </div>
      <div v-if="outsideTemp">
      <p>Temperature: {{Number((outsideTemp).toFixed(1))}}°C</p>
    </div>
    <div v-if="outsideHum">
      <p>Humidity: {{Number((outsideHum).toFixed(1))}}%</p>
    </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data(){
    return {
      joke: '',
      timestamp: '',
      insideTemp: '',
      insideHum: '',
      outsideTemp: '',
      outsideHum: ''
    }
  },
    beforeMount() {
    this.refreshTemps();
  },
  methods: {
    async refreshTemps(){
      let config = {
        headers: {
          'Accept': 'application/json',
          'Origin': 'x-requested-with'
        }
      }
      const joke = await axios.get('https://cors-anywhere.herokuapp.com/http://sprinklesloltemps.ddns.net:8080/sensors/now', config
       ).then(response => {
         this.insideTemp = response.data.inside.temperature,
         this.insideHum = response.data.inside.humidity,
         this.outsideTemp = response.data.outside.temperature,
         this.outsideHum = response.data.outside.humidity,
         this.timestamp  = response.data.timestamp,
         this.joke = joke.data.timestamp;
       });
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->

<style scoped>
.hello {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
  background: #e2e1e0;
  text-align: center;
}

.card {
  font-size: 1.75em;
  color: #2c3e50;
  background: lavender;
  border-radius: 25px;
  display: inline-block;
  height: 400px;
  margin: 1rem;
  position: relative;
  width: 40%;
}
.card-1 {
  box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
  transition: all 0.3s cubic-bezier(.25,.8,.25,1);
}
.card-1:hover {
  box-shadow: 0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22);
}
</style>
