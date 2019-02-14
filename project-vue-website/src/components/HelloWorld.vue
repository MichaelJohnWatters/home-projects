<template>
  <div class="hello">
    <h2>Most Recent Temperatures</h2>
    <h3>Inisde Temperature:</h3>
    <h3>Inside Humdity:</h3>
    <h3>Outside Temperature:</h3>
    <h3>Outside Humdity:</h3>
    <div v-if="joke">
      <p>{{joke}}</p>
    </div>
    <br/>
    <button @click="refreshTemps()">refresh</button>
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
      joke: ''
    }
  },
    beforeMount() {
    this.refreshTemps();
  },
  methods: {
    async refreshTemps(){
      const {
        joke: { photos }
      } = await axios({
        url: "http://192.168.1.218:80/sensors/now",
        headers: {
          Accept: "application/json"
        }
      });
      this.joke = photos[0]
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
