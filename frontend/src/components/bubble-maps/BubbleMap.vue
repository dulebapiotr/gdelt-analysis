<template>
  <div class="bubble-map fill-height" id="mapp"/>
</template>

<script>
import 'amcharts3'
import 'amcharts3/amcharts/plugins/responsive/responsive.js'
import 'amcharts3/amcharts/serial.js'
import 'amcharts3/amcharts/themes/light'

import 'ammap3'
import 'ammap3/ammap/maps/js/worldLow'

export default {
  name: 'bubble-map',

  props: ['map-data'],

  methods: {
    drawMap (bubbleMapData) {
      /* global AmCharts */
      //const minBulletSize = 3
      //const maxBulletSize = 70
      //let min = Infinity
      //let max = -Infinity
      AmCharts.theme = AmCharts.themes.light

      // build map
      const map = new AmCharts.AmMap()

      map.projection = 'winkel3'
      map.addTitle('Population of the World in 2011', 14, 1, 1, false)
      map.addTitle('source: Gapminder', 11, 1, 1, 1, false)
      map.areasSettings = {
        unlistedAreasColor: '#eee',
        unlistedAreasAlpha: 1,
        outlineColor: '#fff',
        outlineThickness: 2,
      }
      map.imagesSettings = {
        balloonText: '<span style="font-size:14px"><b>[[title]]</b>: [[value]]</span>',
        alpha: 0.75,
      }

      const dataProvider = {
        mapVar: AmCharts.maps.worldLow,
        images: [],
      }

      // create circle for each country
      // it's better to use circle square to show difference between values, not a radius
      //const maxSquare = maxBulletSize * maxBulletSize * 2 * Math.PI
      //const minSquare = minBulletSize * minBulletSize * 2 * Math.PI

      console.log("data",bubbleMapData);
      // create circle for each country
      bubbleMapData.forEach((dataItem) => {
        console.log(dataItem);
        //const value = dataItem.value
        // calculate size of a bubble
        //let square = (value - min) / (max - min) * (maxSquare - minSquare) + minSquare
        //if (square < minSquare) {
        //  square = minSquare
        //}
        //const size = Math.sqrt(square / (Math.PI * 2))
        //const id = dataItem.code
        dataProvider.images.push({
          type: 'circle',
          width: 10,
          height: 10,
          color: '#FFAA00',
          longitude: dataItem[1],
          latitude: dataItem[0],
          title: "point",
          value: 1,
        })
      })
      console.log(dataProvider.images);

      map.dataProvider = dataProvider
      map.write(this.$el)
      console.log("koniec");
      console.log(this);
      console.log(map);
      console.log("koniec");
    },
  },
  mounted () {
    //console.log("dziala");
    //console.log(this);
    //var i;
    //while(this.$parent.$parent.$parent.bubbleMapData == null){
    //  i=i+1;
    //}
    //this.drawMap(this.bubbleMapData);
    //console.log(this);
  },
}
</script>
