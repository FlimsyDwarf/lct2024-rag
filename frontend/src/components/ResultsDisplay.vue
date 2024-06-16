<template>
  <v-container>
    <v-card id="results">
      <v-card-title>Analysis Results</v-card-title>
      <v-card-text v-if="results">
        <v-chip
            small
            color="purple"
            class="white--text mb-2"
        >
          <v-icon left>mdi-file</v-icon>
          results.docx
        </v-chip>
      </v-card-text>
      <div class="bar" v-if="showBar">
        <v-progress-linear color="var(--btn-color)" indeterminate  :height="10"></v-progress-linear>
      </div>
      <v-card-actions class="btn-download" v-if="results">
        <v-btn @click="download">Download Results</v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: 'ResultsDisplay',
  data() {
    return {
      results: false,
      showBar: false,
      suffix: '',
    }
  },
  beforeMount() {
    this.$root.$on('onUpdateResults', (response) => {
      this.results = true;
      this.suffix = response.data['OK']
      this.$root.$emit("onChangeBarStatus");
    });

    this.$root.$on("onChangeBarStatus", () => {
      this.showBar = !this.showBar;
      if (this.showBar) {
        this.results = false;
      }
    });
  },
  methods: {
    download() {
      const formData = new FormData();
      formData.append('suffix', this.suffix);
      console.log('downloading')
      axios({
        method: 'POST',
        url: 'http://79.132.136.168:5001/api/1/download_result', //your url
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        data: {
          suffix: this.suffix,
        },
        responseType: 'blob', // important
      }).then((response) => {
        // create file link in browser's memory
        const href = URL.createObjectURL(response.data);
        // create "a" HTML element with href to file & click
        const link = document.createElement('a');
        link.href = href;
        link.setAttribute('download', 'results.docx');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(href);
      });
    }
  },
};
</script>

<style scoped>
#results {
  background-color: var(--bottom-color);
  color: black;
  width: 100%;
}

.v-card-text {
  color: #09002B!important;
}

.results-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}
pre {
  color: black!important;
  white-space: pre-wrap; /* Allows long text to wrap */
  word-wrap: break-word; /* Prevents overflow */
}

.btn-download {
  padding-top: 16px!important;
}

.bar {
  padding: 8px;
}
</style>
