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

const tableHeader = ref([])
const tableData = ref([])

onMounted(() => {
    emitter.on('setHeader', (e) => {
        console.log('setHeader', e)
        for (let i = 0; i < e.length; i++) {
            tableHeader.value.push(e[i])
        }
    })
    emitter.on('featureOneResult', (e) => {
        // console.log('featureOneResult', e)
        let tableItem = e
        if (e.harmonicWaveList[0].code == 1) {
            for (let i = 1; i <= e.harmonicWaveList.length; i++) {
                let str = i + "_Harmonic"
                tableItem[str] = e.harmonicWaveList[i][value]
            }
        }
        delete tableItem.harmonicWaveList
        tableData.value.push(tableItem)
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
  