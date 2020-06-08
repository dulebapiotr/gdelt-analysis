<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>GDELT</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.search-modal>Search</button>
        <br><br>
        <b-spinner v-if="loading" style="margin: auto; width: 5rem; height: 5rem;" label="Large Spinner"></b-spinner>
        <br>
        <div id="arc" />
        <line-chart v-if="showDataPoly" :data="dataPoly" />
        <radial-menu
      style="margin: auto; margin-top: 300px; background-color: red"
      :itemSize="150"
      :radius="240"
      :angle-restriction="360"
      v-if="showMenu">

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
        <radial-menu-item
          style="background-color: white"
          >
          <span v-b-modal.polynomial-fit>polynomial fit</span>
        </radial-menu-item>
        <radial-menu-item
          style="background-color: white"
          >
          <span v-b-modal.mean-std-var>mean std var</span>
        </radial-menu-item>
        <radial-menu-item
          style="background-color: white"
          >
          <span v-b-modal.median>median</span>
        </radial-menu-item>
        <radial-menu-item
          style="background-color: white"
          >
          <span v-b-modal.range-ptp>range ptp</span>
        </radial-menu-item>
        <radial-menu-item
          style="background-color: white"
          >
          <span v-b-modal.percentile>percentile</span>
        </radial-menu-item>
      </radial-menu>
    </div>
  </div>





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
            <select id="form-columnName-input"
                            v-model="valueInTimeForm.column_name">
              <option>FractionDate</option>
              <option>QuadClass</option>
              <option>GoldsteinScale</option>
              <option>NumMentions</option>
              <option>NumSources</option>
              <option>NumArticles</option>
              <option>AvgTone</option>
              <option>Actor1Geo_Type</option>
              <option>Actor1Geo_FeatureID</option>
              <option>DATEADDED</option>
              <option>Actor2Geo_Type</option>
              <option>Actor2Geo_FeatureID</option>
            </select>
          </b-form-group>

          <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
          </b-button-group>
        </b-form>
      </b-modal>

      <b-modal ref="polynomialFitModal"
         id="polynomial-fit"
         title="polynomial fit"
         hide-footer>
        <b-form @submit="onSubmitPolynomialFit">
          <b-form-group id="form-calumnName-group"
                      label="Column Name:"
                      label-for="form-columnName-input">
            <select id="form-columnName-input"
                            v-model="polynomialFitForm.column_name">
              <option>FractionDate</option>
              <option>QuadClass</option>
              <option>GoldsteinScale</option>
              <option>NumMentions</option>
              <option>NumSources</option>
              <option>NumArticles</option>
              <option>AvgTone</option>
              <option>Actor1Geo_Type</option>
              <option>Actor1Geo_FeatureID</option>
              <option>DATEADDED</option>
              <option>Actor2Geo_Type</option>
              <option>Actor2Geo_FeatureID</option>
            </select>
          </b-form-group>
          <b-form-group id="form-degree-group"
                      label="Degree:"
                      label-for="form-degree-input">
            <input id="form-degree-input"
                            v-model="polynomialFitForm.degree"
                            required/>
          </b-form-group>

          <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
          </b-button-group>
        </b-form>
      </b-modal>

      <b-modal ref="meanStdVarModal"
         id="mean-std-var"
         title="Mean std var"
         hide-footer>
        <b-form @submit="onSubmitMeanStdVar">
          <b-form-group id="form-calumnName-group"
                      label="Column Name:"
                      label-for="form-columnName-input">
            <select id="form-columnName-input"
                            v-model="meanStdVarForm.column_name">
              <option>FractionDate</option>
              <option>QuadClass</option>
              <option>GoldsteinScale</option>
              <option>NumMentions</option>
              <option>NumSources</option>
              <option>NumArticles</option>
              <option>AvgTone</option>
              <option>Actor1Geo_Type</option>
              <option>Actor1Geo_FeatureID</option>
              <option>DATEADDED</option>
              <option>Actor2Geo_Type</option>
              <option>Actor2Geo_FeatureID</option>
            </select>
          </b-form-group>

          <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
          </b-button-group>
        </b-form>
      </b-modal>

      <b-modal ref="medianModal"
         id="median"
         title="Median"
         hide-footer>
        <b-form @submit="onSubmitMedian">
          <b-form-group id="form-calumnName-group"
                      label="Column Name:"
                      label-for="form-columnName-input">
            <select id="form-columnName-input"
                            v-model="medianForm.column_name">
              <option>FractionDate</option>
              <option>QuadClass</option>
              <option>GoldsteinScale</option>
              <option>NumMentions</option>
              <option>NumSources</option>
              <option>NumArticles</option>
              <option>AvgTone</option>
              <option>Actor1Geo_Type</option>
              <option>Actor1Geo_FeatureID</option>
              <option>DATEADDED</option>
              <option>Actor2Geo_Type</option>
              <option>Actor2Geo_FeatureID</option>
            </select>
          </b-form-group>

          <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
          </b-button-group>
        </b-form>
      </b-modal>

      <b-modal ref="rangePtpModal"
         id="range-ptp"
         title="Range ptp"
         hide-footer>
        <b-form @submit="onSubmitMedian">
          <b-form-group id="form-calumnName-group"
                      label="Column Name:"
                      label-for="form-columnName-input">
            <select id="form-columnName-input"
                            v-model="rangePtpForm.column_name">
              <option>FractionDate</option>
              <option>QuadClass</option>
              <option>GoldsteinScale</option>
              <option>NumMentions</option>
              <option>NumSources</option>
              <option>NumArticles</option>
              <option>AvgTone</option>
              <option>Actor1Geo_Type</option>
              <option>Actor1Geo_FeatureID</option>
              <option>DATEADDED</option>
              <option>Actor2Geo_Type</option>
              <option>Actor2Geo_FeatureID</option>
            </select>
          </b-form-group>

          <b-button-group>
            <b-button type="submit" variant="primary">Submit</b-button>
          </b-button-group>
        </b-form>
      </b-modal>

      <b-modal ref="percentileModal"
         id="percentile"
         title="Percentile"
         hide-footer>
        <b-form @submit="onSubmitPercentile">
          <b-form-group id="form-calumnName-group"
                      label="Column Name:"
                      label-for="form-columnName-input">
            <select id="form-columnName-input"
                            v-model="percentileForm.column_name">
              <option>FractionDate</option>
              <option>QuadClass</option>
              <option>GoldsteinScale</option>
              <option>NumMentions</option>
              <option>NumSources</option>
              <option>NumArticles</option>
              <option>AvgTone</option>
              <option>Actor1Geo_Type</option>
              <option>Actor1Geo_FeatureID</option>
              <option>DATEADDED</option>
              <option>Actor2Geo_Type</option>
              <option>Actor2Geo_FeatureID</option>
            </select>
          </b-form-group>
          <b-form-group id="form-percentile-group"
                      label="Percentile:"
                      label-for="form-percentile-input">
            <input id="form-percentile-input"
                            v-model="percentileForm.percentile"
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

import * as d3 from 'd3'

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
      },
      polynomialFitForm: {
        column_name: '',
        degree: ''
      },
      meanStdVarForm: {
        column_name: ''
      },
      medianForm: {
        column_name: ''
      },
      rangePtpForm: {
        column_name: ''
      },
      percentileForm: {
        column_name: '',
        percentile: ''
      },
      loading: false,
      showMenu: false,
      width: 1400,
      height: 900,
      margin: 40,
      svg: null,
      dataPoly: [],
      showDataPoly: false
    }
  },
  methods: {
    postPost(payload) {
      axios.post(`http://localhost:5000/new_session`, payload)
      .then(response => {
        this.loading = false;
        this.showMenu = true;
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
        this.polynomialFitForm.calumnName = '';
        this.polynomialFitForm.degree = '';
        this.meanStdVarForm.column_name = '';
        this.medianForm.column_name = '';
        this.rangePtpForm.column_name = '';
        this.percentileForm.column_name = '';
        this.percentileForm.percentile = '';
      },
    onSubmit(evt) {
      evt.preventDefault();
      this.loading = true;
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
      this.loading = true;
      const payload = {
        params: {
          event_type: this.countEventsForm.event_type
        },
        df_name: "raw_result",
        analysis_name: "count_events"
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        this.loading = false;
        console.log(response.data);
        this.data = response.data ;

        var cameo = this.countEventsForm.event_type
        var cameo_labels = ["Make public statement", "Appeal", "Express intent to cooperate", "Consult", "Enagage in diplomatic cooperation", "Engage in material cooperation", "Prove Aid", "Yield", "Investigate", "Demand", "Disapprove", "Reject", "Threaten", "Protest", "Exhibit force posture", "Reduce relations", "Coerce", "Assault", "Fight", "Use mass violence"];
        var caemo_name = cameo_labels[cameo]
        window.alert("CAMEO: "+cameo+"\n Rodzaj wydarzenia: "+caemo_name+"\n Ilość zdarzeń : "+response.data)




      })
      .catch(e => {
        console.log(e);
      })
    },
    onSubmitEventTypesRatio() {
      this.loading = true;
      const payload = {
        df_name: "raw_result",
        analysis_name: "event_types_ratio",
        params: {}
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        console.log(response)
        this.loading = false;
        var radius =  Math.min(this.width, this.height) / 2 - this.margin;
        if(this.svg == null) {
          this.svg = d3.select("#arc")
            .append("svg")
              .attr("width", this.width)
              .attr("height", this.height)
            .append("g")
              .attr("transform", "translate(" + this.width / 2 + "," + this.height / 2 + ")")

        }

        var cameo_labels = ["Make public statement", "Appeal", "Express intent to cooperate", "Consult", "Enagage in diplomatic cooperation", "Engage in material cooperation", "Prove Aid", "Yield", "Investigate", "Demand", "Disapprove", "Reject", "Threaten", "Protest", "Exhibit force posture", "Reduce relations", "Coerce", "Assault", "Fight", "Use mass violence"];

        // set the color scale
        var color = d3.scaleOrdinal()
          .domain(response.data.map(x => x.event_type_cameo))
          .range(d3.schemeDark2);

        // Compute the position of each group on the pie:
        var pie = d3.pie()
          .sort(null) // Do not sort group by size
          .value(function(d) {return d.count; })
        var data_ready = pie(response.data)
        data_ready.forEach(cameoFunction);
        function cameoFunction(value, index){
          data_ready[index].cameo_label = cameo_labels[index] + " " + (data_ready[index].data.ratio*100).toString().substring(0,5)  + '%'
        }
        console.log(data_ready)


        // The arc generator
        var arc = d3.arc()
          .innerRadius(radius * 0.0)         // This is the size of the donut hole
          .outerRadius(radius * 0.8)

        // Another arc that won't be drawn. Just for labels positioning
        var outerArc = d3.arc()
          .innerRadius(radius * 0.9)
          .outerRadius(radius * 0.9)

        // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
        this.svg
          .selectAll('allSlices')
          .data(data_ready)
          .enter()
          .append('path')
          .attr('d', arc)
          .attr('fill', function(d){ return(color(d.cameo_label)) })
          .attr("stroke", "white")
          .style("stroke-width", "2px")
          .style("opacity", 0.7)

        // Add the polylines between chart and labels:
        this.svg
          .selectAll('allPolylines')
          .data(data_ready)
          .enter()
          .append('polyline')
            .attr("stroke", "black")
            .style("fill", "none")
            .attr("stroke-width", 1)
            .attr('points', function(d) {
              var posA = arc.centroid(d) // line insertion in the slice
              var posB = outerArc.centroid(d) // line break: we use the other arc generator that has been built only for that
              var posC = outerArc.centroid(d); // Label position = almost the same as posB
              var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 // we need the angle to see if the X position will be at the extreme right or extreme left
              posC[0] = radius * 0.95 * (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
              return [posA, posB, posC]
            })

        // Add the polylines between chart and labels:
        this.svg
          .selectAll('allLabels')
          .data(data_ready)
          .enter()
          .append('text')
            .text( function(d) { console.log(d.data.event_type_cameo) ; return d.cameo_label } )
            .attr('transform', function(d) {
                var pos = outerArc.centroid(d);
                var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
                pos[0] = radius * 0.99 * (midangle < Math.PI ? 1 : -1);
                return 'translate(' + pos + ')';
            })
            .style('text-anchor', function(d) {
                var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
                return (midangle < Math.PI ? 'start' : 'end')
            })
      })
      .catch(e => {
        console.log(e);
      })
    },
    onSubmitValueInTime(evt) {
      evt.preventDefault();
      this.$refs.valueInTimeModal.hide();
      this.loading = true;
      const payload = {
        df_name: "raw_result",
        analysis_name: "value_in_time",
        params: {
          value: this.valueInTimeForm.column_name
        }
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        this.loading = false;
        console.log(response.data);
        this.data = response.data;
      })
      .catch(e => {
        console.log(e);
      })
    },
    onSubmitPolynomialFit(evt) {
      evt.preventDefault();
      this.$refs.polynomialFitModal.hide();
      this.loading = true;
      const payload = {
        df_name: "raw_result",
        analysis_name: "polynomial_fit",
        params: {
          column_name: this.polynomialFitForm.column_name,
          degree: this.polynomialFitForm.degree
        }
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        this.loading = false;
        console.log(response.data);
        function lol(val) {
          var toReduce = response.data.map((x, index) => {
            return x* Math.pow(val, index);
          });
          var sum = 0;
          for(var x of toReduce) {
            sum += x;
          }
          return sum
        }
        var list = [];
        for (var i = -10; i <= 10; i++) {
            list.push(i);
        }

        var dataa = []

        for(i of list) {
          dataa.push([i, lol(i)]);
        }
        this.dataPoly = [
  {name: this.polynomialFitForm.column_name, data: dataa}
];
this.showDataPoly = true;

// an
      })
      .catch(e => {
        console.log(e);
      })
    },
    onSubmitMeanStdVar(evt) {
      evt.preventDefault();
      this.$refs.meanStdVarModal.hide();
      this.loading = true;
      const payload = {
        df_name: "raw_result",
        analysis_name: "mean_std_var",
        params: {
          column_name: this.meanStdVarForm.column_name,
        }
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        var mean = response.data.mean;
        var std_dev = response.data.std_dev;
        var variance = response.data.variance;
        window.alert("Column: " + this.meanStdVarForm.column_name + "\n Mean: " + mean + "\n Standard deviation: " + std_dev + "\n Variance: " + variance);
        this.loading = false;
        console.log(response.data);
        this.data = response.data;
      })
      .catch(e => {
        console.log(e);
      })
    },
    onSubmitMedian(evt) {
      evt.preventDefault();
      this.$refs.medianModal.hide();
      this.loading = true;
      const payload = {
        df_name: "raw_result",
        analysis_name: "median",
        params: {
          column_name: this.medianForm.column_name,
        }
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        this.loading = false;
        console.log(response.data);
        this.data = response.data;
      })
      .catch(e => {
        console.log(e);
      })
    },
    onSubmitRangePtp(evt) {
      evt.preventDefault();
      this.$refs.rangePtpModal.hide();
      this.loading = true;
      const payload = {
        df_name: "raw_result",
        analysis_name: "range_ptp",
        params: {
          column_name: this.range_ptp.column_name,
        }
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        this.loading = false;
        console.log(response.data);
        this.data = response.data;
      })
      .catch(e => {
        console.log(e);
      })
    },
    onSubmitPercentile(evt) {
      evt.preventDefault();
      this.$refs.percentileModal.hide();
      this.loading = true;
      const payload = {
        df_name: "raw_result",
        analysis_name: "percentile",
        params: {
          column_name: this.percentileForm.column_name,
          percentile: this.percentileForm.percentile
        }
      };
      axios.post(`http://localhost:5000/add_analysis`, payload)
      .then(response => {
        window.alert("Column: " + this.percentileForm.column_name + "\nPercentile: " + this.percentileForm.percentile + "\nResult: " + response.data);
        this.loading = false;
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
