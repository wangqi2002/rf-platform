<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div class="box">
      <button class="btn" @click="handleFPHCS1">FPHGCS</button>
      <button class="btn" @click="handleFPHCS2">FPHPCS</button>
      <button class="btn" @click="handleRDGCS1">RDGGCS</button>
      <button class="btn" @click="handleRDGCS2">RDGPCS</button>
      <button class="btn" @click="handleRDSCS1">RDSGCS</button>
      <button class="btn" @click="handleRDSCS2">RDSPCS</button>
      <button class="btn" @click="handleAMPCS1">AMPGCS</button>
      <button class="btn" @click="handleAMPCS2">AMPPCS</button>
      <button class="btn" @click="handleFeature">Feature</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, getCurrentInstance } from "vue"
import fphApi from "../api/fphApi"
import ampApi from "../api/ampApi"
import rigol_dg4062 from "../api/rigol_dg4062"
import rigol_ds4014 from "../api/rigol_ds4014"
import appApi from "../api/appApi"

const { proxy } = getCurrentInstance()

const msg = ref('hello world')


const handleFeature = () => {
  console.log(appApi.FeatureOne())
}
const handleFPHCS1 = () => {
  console.log(fphApi.gcs1({ cs: 'gcs1' }))
}
const handleFPHCS2 = () => {
  console.log(fphApi.pcs1({ cs: 'pcs1' }))
}
const handleRDGCS1 = () => {
  console.log(rigol_dg4062.gcs1({ cs: 'gcs1' }))
}
const handleRDGCS2 = () => {
  console.log(rigol_dg4062.pcs1({ cs: 'pcs1' }))
}
const handleRDSCS1 = () => {
  console.log(rigol_ds4014.gcs1({ cs: 'gcs1' }))
}
const handleRDSCS2 = () => {
  console.log(rigol_ds4014.pcs1({ cs: 'pcs1' }))
}
const handleAMPCS1 = () => {
  console.log(ampApi.gcs1({ cs: 'gcs1' }))
}
const handleAMPCS2 = () => {
  console.log(ampApi.pcs1({ cs: 'pcs1' }))
}
const init = () => {
  // proxy.$socket.emit('message', "hhhhhhhhh");
}
onMounted(() => {
  // proxy.$socket.on('my_response_message', (data) => {
  //   console.log(data)
  // });
})
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.hello {
  width: 100%;
  height: 100%;

  .box {
    width: 100vw;
    height: 200px;
    background-color: aliceblue;

    .btn {
      width: 120px;
      height: 40px;
      margin: 10px;
      background-color: antiquewhite;
      border: none;
      border-radius: 5px;
    }
  }
}
</style>
