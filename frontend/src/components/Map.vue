<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>MAPS</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.map-search-modal1>Events <br> between countries</button>
        
        <br><br>
      </div>
    </div>

    <b-modal ref="mapSearchDataframeModal1"
         id="map-search-modal1"
         title="Events between countries"
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
          <b-button type="submit1" variant="primary">Submit</b-button>
          <b-button type="reset1" variant="danger">Reset</b-button>
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
         class="col-sm-12"
         size="xl"
         hide-footer>          
         <bubble-map
            :map-data="bubbleMapData"
            style="height: 80vh;"
          />
    </b-modal>

  </div>
</template>

<script>
import axios from 'axios';
import Datepicker from 'vuejs-datepicker';
import BubbleMap from './bubble-maps/BubbleMap'

// import * as d3 from 'd3'

export default {
  name: 'Map',
  components: {
    Datepicker,
    BubbleMap,
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
      bubbleMapData: "",
      data: null
    }
  },
  methods: {

    getMap1(payload) {
      this.$refs.bubbleMapModal.show();
      //console.log(this.$refs.bubbleMapModal);
      //console.log(this.$refs);
      //console.log(this);
      //this.$refs.bubbleMapModal.$children[0].$children[0].drawMap(null);
      axios.post(`http://localhost:5000/actors-action-geo`, payload)
      .then(response => {
        //this.bubbleMapData = response.data;
        this.$refs.bubbleMapModal.$children[0].$children[0].drawMap(response.data);
        console.log(response.data);
        //console.log(this.$refs.bubbleMapModal);
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
