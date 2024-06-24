<template>
  <v-container class="home-container " fluid>
    <v-row no-gutters class="top-section fill-space">
      <v-col cols="12">
        <Settings />
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col cols="12" class="bottom-section fill-space">
        <ResultsDisplay />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Settings from '@/components/Settings.vue';
import ResultsDisplay from '@/components/ResultsDisplay.vue';

export default {
  name: 'HomeComponent',
  components: {
    Settings,
    ResultsDisplay,
  },
};
</script>

<style scoped>



</style>
