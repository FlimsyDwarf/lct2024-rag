<template>
  <v-app-bar flat class="bar" color="#09002B">
    <v-toolbar-title>AI-Powered Data Analysis</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-btn >Contacts</v-btn>
    </v-toolbar-items>
  </v-app-bar>
</template>

<script>
export default {
  name: "HeaderComponent"
};
</script>

<style scoped>
.v-btn {
  background-color: var(--top-color)!important;
}
/* Add any custom styles here */
</style>
