<template>
  <div>
    <svg id="geo_svg" style="border: 1px lightgray solid"></svg>
  </div>
</template>
<style>
#geo_svg {
  background: lightblue;
}

.county {
  fill: #ebf0e4;
  stroke: gray;
  stroke-width: 0.4px;
}

.county:hover {
  fill: lightgray;
}
</style>

<script setup lang="ts">
import { ref, onMounted } from "vue";

import * as d3 from "d3";
import * as topojson from "topojson";
import { F } from "../utils/F";
import { Env } from "../defines/env";

async function draw() {
  const width = F.canvasWidth();
  const svg = d3.select("#geo_svg").attr("width", width).attr("height", 500);
  const g = svg.append("g");

  const [jsondata, aaa] = await Promise.all([
    d3.json("COUNTY_MOI_1090820.json"),
    d3.json(`${Env.APIHOST}/accident/geo`),
  ]);

  const projectmethod = d3
    .geoMercator()
    .center([123 - 2.2, 24 + 0.25])
    .scale(10000 * 7);
  const pathGenerator = d3.geoPath().projection(projectmethod);

  // 地圖的檔案先讀取
  const geometries = (topojson as any).feature(
    jsondata,
    jsondata.objects["COUNTY_MOI_1090820"]
  );
  g.append("path");
  const paths = g.selectAll("path").data(geometries.features);
  paths.enter().append("path").attr("d", pathGenerator).attr("class", "county");

  // 場館的檔案後讀取
  g.selectAll("circle")
    .data(aaa.data)
    .enter()
    .append("circle")
    .attr("cx", function (d) {
      return projectmethod([d.x, d.y])[0];
    })
    .attr("cy", function (d) {
      return projectmethod([d.x, d.y])[1];
    })
    .attr("r", 1)
    .style("fill", "red");
}

onMounted(() => {
  draw();
});
</script>
