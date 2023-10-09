<template>
  <center>
    <H1>臺中市政府警察局112年7月份交通事故資料</H1>
    <hr />
    <H3>尖峰時刻</H3>
    <RushHour />
    <hr width="70%" />
    <H3>各區競賽累積事故量</H3>
    <DayByDay />
    <hr width="70%" />
    <H3>事故分佈圖</H3>
    <Geo />
    <hr width="70%" />
    <H3>各區事故量</H3>
    <DistrictAccident />
    <hr width="70%" />
    <H3>事故類型</H3>
    <AccidentGroupbyType />

    <!-- <Weather /> -->
  </center>
</template>

<script setup lang="ts">
import Geo from "./Geo.vue";
import RushHour from "./RushHour.vue";
import Weather from "./Weather.vue";
import DayByDay from "./DayByDay.vue";
import AccidentGroupbyType from "./AccidentGroupbyType.vue";
import DistrictAccident from "./DistrictAccident.vue";
</script>
