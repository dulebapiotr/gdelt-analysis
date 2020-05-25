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

// import * as d3 from 'd3'

export default {
  name: 'Chart',
  components: {
    Datepicker
  },
  // props: {
  //   data: Object
  // },
  data() {
    return {
      searchDataframeForm: {
        start: '',
        stop: '',
      },
      data: null
    }
  },
  methods: {
    postPost(payload) {
      axios.post(`http://localhost:5000/dataframes`, payload)
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
