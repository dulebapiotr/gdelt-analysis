<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>GDELT</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.search-modal>Search</button>
        <br><br>
      </div>
    </div>

    <svg>
    </svg>
    <radial-menu
      style="margin: auto; margin-top: 300px; background-color: red"
      :itemSize="150"
      :radius="240"
      :angle-restriction="360">
        <radial-menu-item
          style="background-color: white"
          >
          <span v-b-modal.count-events>count events</span>
        </radial-menu-item>
        <radial-menu-item
          style="background-color: white"
          @click="() => onSubmitEventTypesRatio()"
          >
          <span>event types ratio</span>
        </radial-menu-item>
        <radial-menu-item
          style="background-color: white"
          >
          <span v-b-modal.value-in-time>value in time</span>
        </radial-menu-item>
      </radial-menu>


      <b-modal ref="countEventsModal"
         id="count-events"
         title="count Events"
         hide-footer>
        <b-form @submit="onSubmitCountEvents">
          <b-form-group id="form-eventType-group"
                      label="Event Type:"
                      label-for="form-eventType-input">
            <input id="form-eventType-input"
                            v-model="countEventsForm.event_type"
                            required/>
          </b-form-group>

          <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
          </b-button-group>
        </b-form>
      </b-modal>

      <b-modal ref="valueInTimeModal"
         id="value-in-time"
         title="value in time"
         hide-footer>
        <b-form @submit="onSubmitValueInTime">
          <b-form-group id="form-calumnName-group"
                      label="Column Name:"
                      label-for="form-columnName-input">
            <input id="form-columnName-input"
                            v-model="valueInTimeForm.column_name"
                            required/>
          </b-form-group>

          <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
          </b-button-group>
        </b-form>
      </b-modal>

    <b-modal ref="searchDataframeModal"
         id="search-modal"
         title="Search a Dataframe"
         hide-footer>
      <b-form @submit="onSubmit" @reset="onReset">
        <b-form-group id="form-start-group"
                    label="Start:"
                    label-for="form-start-input">
          <Datepicker id="form-start-input"
                          v-model="searchDataframeForm.start"
                          required>
          </Datepicker>
        </b-form-group>
        <b-form-group id="form-stop-group"
                      label="Stop:"
                      label-for="form-stop-input">
            <Datepicker id="form-stop-input"
                            v-model="searchDataframeForm.stop"
                            required>
            </Datepicker>
          </b-form-group>

        <b-button-group>
          <b-button type="submit" variant="primary">Submit</b-button>
          <b-button type="reset" variant="danger">Reset</b-button>
        </b-button-group>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Datepicker from 'vuejs-datepicker';
import { RadialMenu,  RadialMenuItem } from 'vue-radial-menu'

// import * as d3 from 'd3'

export default {
  name: 'Chart',
  components: {
    Datepicker,
    RadialMenu,
    RadialMenuItem
  },
  // props: {
  //   data: Object
  // },
  data() {
    return {
      searchDataframeForm: {
        start: '',
        stop: '',
        actorCameo: ''
      },
      data: null,
      showModalCountEvents: false,
      countEventsForm: {
        event_type: ''
      },
      valueInTimeForm: {
        column_name: ''
      }
    }
  },
  methods: {
    postPost(payload) {
      axios.post(`http://localhost:5000/new_session`, payload)
      .then(response => {
        console.log(response.data);
        this.data = response.data;
      })
      .catch(e => {
        console.log(e);
      })
    },
    initForm() {
        this.searchDataframeForm.start = '';
        this.searchDataframeForm.stop = '';
        this.countEventsForm.event_type = '';
        this.valueInTimeForm.column_name = '';
      },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.searchDataframeModal.hide();
      const payload = {
        start: this.searchDataframeForm.start,
        stop: this.searchDataframeForm.stop
      };
      this.postPost(payload);
    },
    onSubmitCountEvents(evt) {
      evt.preventDefault();
      this.$refs.countEventsModal.hide();
      const payload = {
        params: {
          event_type: this.countEventsForm.event_type
        },
        df_name: "raw_result",
        analysis_name: "count_events"
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        console.log(response.data);
        this.data = response.data;
      })
      .catch(e => {
        console.log(e);
      })
    },
    onSubmitEventTypesRatio() {
      const payload = {
        df_name: "raw_result",
        analysis_name: "event_types_ratio",
        params: {}
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        console.log(response.data);
        this.data = response.data;
      })
      .catch(e => {
        console.log(e);
      })
    },
    onSubmitValueInTime(evt) {
      evt.preventDefault();
      const payload = {
        df_name: "raw_result",
        analysis_name: "value_in_time",
        params: {
          value: this.valueInTimeForm.column_name
        }
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        console.log(response.data);
        this.data = response.data;
      })
      .catch(e => {
        console.log(e);
      })
    },
    onReset(evt) {
        evt.preventDefault();
        this.$refs.searchDataframeModal.hide();
        this.initForm();
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
