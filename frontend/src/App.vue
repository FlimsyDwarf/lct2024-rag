<template>
  <v-app>
    <Header class="header" />
    <v-main>
      <Home />
    </v-main>
  </v-app>
</template>

<script>
import Header from '@/components/Header.vue';
import Home from '@/components/page/Home.vue';
import axios from "axios"

export default {
  name: 'App',
  components: {
    Header,
    Home,
  },
  beforeCreate() {
    this.$root.$on("onMakeRequest", (userSources, amountOfLinks, dateRange, useInternet, template, files) => {
      try {
        const formData = new FormData();
        if (template == null) {
          this.$root.$emit("onRequestError", "template is required");
        } else {
          this.$root.$emit("onChangeBarStatus");
          formData.append('template', template);
          if (files !== null) {
            files.forEach((file, index) => {
              formData.append('file' + index, file);
            });
          }
          if (userSources !== null) {
            formData.append('userSources', userSources.map(source => source.value));
          }
          if (dateRange !== null) {
            formData.append('dateRange', dateRange);
          }
          if (useInternet !== null) {
            formData.append('useInternet', useInternet);
          } else {
            formData.append('useInternet', false);
          }
          formData.append('amountOfLinks', amountOfLinks);

          // Send settings and file to the backend in a single request
          axios.post('http://79.132.136.168:5001/api/1/make_request', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }).then(response => {
            console.log(response);
            this.$root.$emit("onUpdateResults", response);
          }).catch((reason) => {
            console.log('ERROR: ', reason);
            this.$root.$emit("onRequestError", "Some problems occurred. Try again.");
            this.$root.$emit("onChangeBarStatus");
          });
        }

      } catch (error) {
        console.error('There was an error applying the settings:', error);
      }
    });

    this.$root.$on("onDownloadTemplate", (id) => {
      console.log('downloading template');
      axios({
        method: 'POST',
        url: 'http://79.132.136.168:5001/api/1/download_template', //your url
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        data: {
          id: id,
        },
        responseType: 'blob', // important
      }).then((response) => {
        // create file link in browser's memory
        const href = URL.createObjectURL(response.data);
        // create "a" HTML element with href to file & click
        const link = document.createElement('a');
        link.href = href;
        link.setAttribute('download', 'template.docx');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(href);
      }).catch(error => {
        console.log('ERROR: ', error);
      });
    });

    this.$root.$on("onDownloadResult", (suffix) => {
      console.log('downloading result')
      axios({
        method: 'POST',
        url: 'http://79.132.136.168:5001/api/1/download_result', //your url
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        data: {
          suffix: suffix,
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
      })
    });
  }
};

</script>

<style>
/* Add any global styles here */
</style>
