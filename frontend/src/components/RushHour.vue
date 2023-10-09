<template>
  <div id="elem-rush-hour"></div>
</template>

<script setup lang="ts">
import axios from "axios";
import { ref, onMounted } from "vue";

import * as d3 from "d3";
import { F } from "../utils/F";
import { Env } from "../defines/env";

function draw(data) {
  document.querySelector("#elem-rush-hour svg")?.remove();

  const width = F.canvasWidth();
  const height = 300;
  const marginTop = 20;
  const marginRight = 20;
  const marginBottom = 30;
  const marginLeft = 40;

  // Bin the data.
  const bins = (d3.bin().thresholds(24) as any).value((d) => {
    // console.log(d);
    return d.hour;
  })(data);

  // Declare the x (horizontal position) scale.
  const x = d3
    .scaleLinear()
    .domain([bins[0].x0, bins[bins.length - 1].x1])
    .range([marginLeft, width - marginRight]);

  // Declare the y (vertical position) scale.
  const y = d3
    .scaleLinear()
    .domain([0, d3.max(bins, (d) => d[0].count)])
    .range([height - marginBottom, marginTop]);

  // Create the SVG container.
  const svg = d3
    .select("#elem-rush-hour")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto;");

  // Add a rect for each bin.
  svg
    .append("g")
    .attr("fill", "steelblue")
    .selectAll()
    .data(bins)
    .join("rect")
    .attr("x", (d) => x(d.x0) + 1)
    .attr("width", (d) => x(d.x1) - x(d.x0) - 1)
    .attr("y", (d) => y(d[0].count))
    .attr("height", (d) => y(0) - y(d[0].count));

  // Add the x-axis and label.
  svg
    .append("g")
    .attr("transform", `translate(0,${height - marginBottom})`)
    .call(d3.axisBottom(x).ticks(24).tickSizeOuter(0))
    .call((g) =>
      g
        .append("text")
        .attr("x", width)
        .attr("y", marginBottom - 4)
        .attr("fill", "currentColor")
        .attr("text-anchor", "end")
        .text("時間/小時")
    );

  // Add the y-axis and label, and remove the domain line.
  svg
    .append("g")
    .attr("transform", `translate(${marginLeft},0)`)
    .call(d3.axisLeft(y).ticks(height / 40))
    .call((g) => g.select(".domain").remove())
    .call((g) =>
      g
        .append("text")
        .attr("x", -marginLeft)
        .attr("y", 10)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .text("事故量")
    );
}

async function getData() {
  const path = `${Env.APIHOST}/statics/rush_hour`;
  try {
    const resp = await axios.get(path);
    draw(resp.data.data);
  } catch (error) {
    console.log(error);
  }
}

onMounted(() => {
  getData();
});
</script>
