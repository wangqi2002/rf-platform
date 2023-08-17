<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div class="box">
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
  // console.log(appApi.FeatureOne())
  console.log(rigol_dg4062.connect({ resource: 'TCPIP0::192.168.2.15::inst0::INSTR' }))
}
onMounted(() => {
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
