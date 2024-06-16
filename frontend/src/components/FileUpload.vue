<template>
  <v-container>
    <Settings />
    <v-container>
    <v-file-input
        label="Upload your data file"
        prepend-icon="mdi-upload"
        @change="handleFileUpload"
    ></v-file-input>
    <v-btn @click="submitFile" color="primary">Upload</v-btn>
    </v-container>
  </v-container>
</template>

<script>
import Settings from './Settings.vue';

export default {
  name: 'FileUpload',
  components: {
    Settings
  },
  methods: {
  },
};
</script>

<style scoped>
/* Add any custom styles here */
</style>
