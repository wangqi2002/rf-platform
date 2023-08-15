<template>
    <div class="table_box">
        <el-table :data="tableData" stripe height="450" style="width: 100%">
            <el-table-column type="index" label="ID" width="40"></el-table-column>
            <el-table-column :prop="item.prop" :label="item.label" width="100" show-overflow-tooltip
                v-for="(item, index) in tableHeader" :key="index"></el-table-column>
        </el-table>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as XLSX from 'xlsx';
import emitter from "../util/mittBus.js"

const tableHeader = ref([
    /* {
        prop: "freq",
        label: "频率"
    },
    {
        prop: "inputPower",
        label: "输入功率"
    },
    {
        prop: "incidentPower",
        label: "入射功率"
    },
    {
        prop: "reflectedPower",
        label: "反射功率"
    },
    {
        prop: "inputSWR",
        label: "输入驻波比"
    } *//* ,
    {
        prop: "directI",
        label: "直流电流"
    },
    {
        prop: "directV",
        label: "直流电压"
    },
    {
        prop: "directP",
        label: "直流功率"
    },
    {
        prop: "outputP",
        label: "输出功率"
    },
    {
        prop: "gain",
        label: "增益"
    },
    {
        prop: "fundamentalWave",
        label: "基波"
    },
    {
        prop: "secondHarmonic",
        label: "二次谐波"
    },
    {
        prop: "thirdHarmonic",
        label: "三次谐波"
    },
    {
        prop: "efficiency",
        label: "效率"
    },
    {
        prop: "harmonicComponent",
        label: "谐波分量"
    } */
])
const tableData = ref([])

onMounted(() => {
    emitter.on('setHeader', (e) => {
        console.log('setHeader', e)
        for (let i = 0; i < e.length; i++) {
            tableHeader.value.push(e[i])
        }
    })
    emitter.on('featureOneResult', (e) => {
        console.log('featureOneResult', e)
        // tableData.value.push(e)
        // let timer = null
        // let count = 0
        // timer = setInterval(() => {
        //     setTimeout(() => {
        //         tableData.value.push(e)
        //         if (count > 20) {
        //             clearInterval(timer)
        //         }
        //     }, 0)
        //     count++
        // }, 1000)
    })
    emitter.on('featureOneSave', () => {
        console.log('featureOneSave')
        const workSheetData = tableData.value;
        const ws = XLSX.utils.json_to_sheet(workSheetData);
        const workSheetName = 'MySheet';
        const workbook = XLSX.utils.book_new();

        XLSX.utils.book_append_sheet(workbook, ws, workSheetName);
        return XLSX.writeFile(workbook, 'feature_one_result.xlsx', { type: 'binary' });
    })
    emitter.on('clearHeader', (e) => {
        console.log('clearHeader', e)
        tableHeader.value.length = 0
    })
})
</script>
  
<style lang="scss">
.table_box {
    width: 100%;
    height: 100%;

    .el-table {
        .cell {
            padding: 0 8px;
        }
    }
}
</style>
  