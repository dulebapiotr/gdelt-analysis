<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>GDELT</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.map-search-modal1>Search</button>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.map-search-modal2>Search</button>
        <br><br>
      </div>
    </div>

    <b-modal ref="mapSearchDataframeModal1"
         id="map-search-modal1"
         title="Search a map Dataframe"
         hide-footer>
      <b-form @submit="onSubmit1" @reset="onReset1">
        <b-form-group id="form-start-group"
                    label="Start:"
                    label-for="form-start-input">
          <Datepicker id="form-start-input"
                          v-model="mapSearchDataframeModal1.start"
                          required>
          </Datepicker>
        </b-form-group>
        <b-form-group id="form-stop-group"
                      label="Stop:"
                      label-for="form-stop-input">
            <Datepicker id="form-stop-input"
                            v-model="mapSearchDataframeModal1.stop"
                            required>
            </Datepicker>
          </b-form-group>
        <b-form-group id="form-actor1-group"
                      label="actor1:"
                      label-for="form-actor1-input">
            <input id="form-actor1-input"
                            v-model="mapSearchDataframeModal1.actor1"
                            required/>
          </b-form-group>
        <b-form-group id="form-actor2-group"
                      label="actor2:"
                      label-for="form-actor2-input">
            <input id="form-actor2-input"
                            v-model="mapSearchDataframeModal1.actor2"
                            required/>
          </b-form-group>

        <b-button-group>
          <b-button type="submit1" variant="primary">Submit1</b-button>
          <b-button type="reset1" variant="danger">Reset1</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal ref="mapSearchDataframeModal2"
         id="map-search-modal2"
         title="Search a map Dataframe2"
         hide-footer>
      <b-form @submit="onSubmit2" @reset="onReset2">
        <b-form-group id="form-start-group"
                    label="Start:"
                    label-for="form-start-input">
          <Datepicker id="form-start-input"
                          v-model="mapSearchDataframeModal2.start"
                          required>
          </Datepicker>
        </b-form-group>
        <b-form-group id="form-stop-group"
                      label="Stop:"
                      label-for="form-stop-input">
            <Datepicker id="form-stop-input"
                            v-model="mapSearchDataframeModal2.stop"
                            required>
            </Datepicker>
          </b-form-group>
        <b-form-group id="form-actor1-group"
                      label="actor1:"
                      label-for="form-actor1-input">
            <input id="form-actor1-input"
                            v-model="mapSearchDataframeModal2.actor1"
                            required/>
          </b-form-group>
        <b-form-group id="form-actor2-group"
                      label="actor2:"
                      label-for="form-actor2-input">
            <input id="form-actor2-input"
                            v-model="mapSearchDataframeModal2.actor2"
                            required/>
          </b-form-group>

        <b-button-group>
          <b-button type="submit2" variant="primary">Submit2</b-button>
          <b-button type="reset2" variant="danger">Reset2</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal ref="bubbleMapModal"
         id="bubble-map-modal"
         title="bubble-map-tittle"
         hide-footer>
        <div class="bubble-map fill-height" />
    </b-modal>

  </div>
</template>

<script>
import axios from 'axios';
import Datepicker from 'vuejs-datepicker';

import 'amcharts3'
import 'amcharts3/amcharts/plugins/responsive/responsive.js'
import 'amcharts3/amcharts/serial.js'
import 'amcharts3/amcharts/themes/light'

import 'ammap3'
import 'ammap3/ammap/maps/js/worldLow'
// import * as d3 from 'd3'

export default {
  name: 'Map',
  components: {
    Datepicker,
  },
  // props: {
  //   data: Object
  // },
  data() {
    return {
      mapSearchDataframeModal1: {
        start: '',
        stop: '',
        actor1: '',
        actor2: '',
      },
      mapSearchDataframeModal2: {
        start: '',
        stop: '',
        actor1: '',
        actor2: '',
      },
      bubbleMapData: null,
      data: null
    }
  },
  methods: {
    drawMap () {
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

      console.log(this.bubbleMapData);
      // create circle for each country
      this.bubbleMapData.forEach((dataItem) => {
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
          width: 1,
          height: 1,
          color: '#FFFFFF',
          longitude: dataItem[1],
          latitude: dataItem[0],
          title: "",
          value: 0,
        })
      })

      map.dataProvider = dataProvider
      map.write(this.$el)
    },
    getMap1(payload) {
      axios.post(`http://localhost:5000/actors-action-geo`, payload)
      .then(response => {
        this.bubbleMapData = response.data
        this.$refs.bubbleMapModal.show();
        this.drawMap();
      })
      .catch(e => {
        console.log(e);
        console.log(payload);
      })
    },
    initForm() {
        this.mapSearchDataframeModal1.start = '';
        this.mapSearchDataframeModal1.stop = '';
        this.mapSearchDataframeModal1.actor1 = '';
        this.mapSearchDataframeModal1.actor2 = '';
        this.mapSearchDataframeModal2.start = '';
        this.mapSearchDataframeModal2.stop = '';
        this.mapSearchDataframeModal2.actor1 = '';
        this.mapSearchDataframeModal2.actor2 = '';
      },
    onSubmit1(evt) {
      evt.preventDefault();
      this.$refs.mapSearchDataframeModal1.hide();
      const payload = {
        start: this.mapSearchDataframeModal1.start,
        stop: this.mapSearchDataframeModal1.stop,
        actor1: this.mapSearchDataframeModal1.actor1,
        actor2: this.mapSearchDataframeModal1.actor2,
      };
      this.getMap1(payload);
    },
    onReset1(evt) {
        evt.preventDefault();
        this.$refs.mapSearchDataframeModal1.hide();
        this.initForm();
      },
    onSubmit2(evt) {
      evt.preventDefault();
      this.$refs.mapSearchDataframeModal2.hide();
      const payload = {
        start: this.mapSearchDataframeModal2.start,
        stop: this.mapSearchDataframeModal2.stop,
        actor1: this.mapSearchDataframeModal2.actor1,
        actor2: this.mapSearchDataframeModal2.actor2,
      };
      this.getMap1(payload);
    },
    onReset2(evt) {
        evt.preventDefault();
        this.$refs.mapSearchDataframeModal2.hide();
        this.initForm();
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
