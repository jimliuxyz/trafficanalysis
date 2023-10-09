<template>
  <div id="word-cloud-graph2"></div>
</template>

<script setup lang="ts">
import axios from "axios";
import { ref, onMounted } from "vue";

import * as d3 from "d3";
import cloud from "d3-cloud";
import { Type } from "../defines/defines";
import { F } from "../utils/F";

const state = ref({
  data: ["Hello", "world"].map(function (d) {
    return { text: d, size: 10 + Math.random() * 90, test: "haha" };
  }),
});

const layout = cloud()
  .size([F.canvasWidth(), 500])
  .words(state.value.data)
  .padding(5)
  .rotate(function (d) {
    return d.size < 10 ? 90 : 0;
  })
  .font("Impact")
  .fontSize(function (d) {
    return d.size;
  })
  .on("end", draw);

function d3_layout() {
  layout.words(state.value.data);
  layout.start();
}

function draw(words) {
  document.querySelector("#word-cloud-graph2 svg")?.remove();

  d3.select("#word-cloud-graph2")
    .append("svg")
    .attr("width", layout.size()[0])
    .attr("height", layout.size()[1])
    .append("g")
    .attr(
      "transform",
      "translate(" + layout.size()[0] / 2 + "," + layout.size()[1] / 2 + ")"
    )
    .selectAll("text")
    .data(words)
    .enter()
    .append("text")
    .style("font-size", function (d) {
      return d.size + "px";
    })
    .style("font-family", "Impact")
    .attr("text-anchor", "middle")
    .attr("transform", function (d) {
      return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
    })
    .text(function (d) {
      return d.text;
    });
}

async function getData() {
  const path = "http://localhost:5001/statics/district_accident";
  try {
    const resp = await axios.get(path);
    // console.log(resp.data.data);
    const data = resp.data.data
      .sort((n1, n2) => n2.count - n1.count)
      .map((d) => {
        return {
          text: d.district + d.count,
          size: Math.pow(d.count, 0.5),
        };
      });
    state.value.data = data;

    d3_layout();
  } catch (error) {
    console.log(error);
  }
}

onMounted(() => {
  getData();
});
</script>
