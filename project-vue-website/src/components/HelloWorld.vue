<template>
  <div class="hello">
    <h2>Most Recent Reads</h2>
    <p>Sensors are read once per minute.</p>
    <p>Both sensors currently inside.</p>
    <div v-if="joke">
      <p>{{joke}}</p>
    </div>
    <div v-if="timestamp">
      <p>Timestamp of last read: {{timestamp}} </p>
    </div>
    <div v-if="insideTemp">
      <p>Inside Temperature: {{insideTemp}}°C </p>
    </div>
      <div v-if="outsideTemp">
      <p>Outside Temperature: {{outsideTemp}}°C </p>
    </div>
    <div v-if="insideHum">
      <p>Inside Humidity: {{insideHum}} % </p>
    </div>
    <div v-if="outsideHum">
      <p><bold>Outside Humidity:</bold> {{outsideHum}} % </p>
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
      outsideHum: '',
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
      const joke = await axios.get('https://cors-anywhere.herokuapp.com/http://sprinklesloltemps.ddns.net:5000/sensors/now', config
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
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
