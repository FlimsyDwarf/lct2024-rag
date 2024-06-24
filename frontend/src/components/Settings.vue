<template>
  <v-container class="settings">
    <!-- Displaying existing settings -->
    <v-list color=var(--top-color) dense style="max-height: 100px"
            class="overflow-y-auto">
      <v-list-item v-for="(userSource, index) in userSources" :key="index">
        <v-list-item-content>
          <v-list-item-title>{{ userSource.value }}</v-list-item-title>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn icon @click="removeUserSource(index)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>

    <v-form>
      <v-text-field
          label="New source"
          v-model="newUserSource"
          color="white"
      ></v-text-field>
      <v-btn @click="addUserSource">Add source</v-btn>

<!--       Date Range Picker-->
      <v-menu
          ref="menu"
          v-model="menu"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="290px"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-text-field
              label="Select Date Range"
              prepend-icon="mdi-calendar"
              readonly
              v-on="on"
              v-bind="attrs"
              color="white"
              :value="dateRange == null ? '' : dateRange.join(' - ')"
          >
          </v-text-field>
        </template>
        <v-date-picker v-model="dateRange" event-color="white" header-color="primary" range>
          <v-btn text @click="dateRange = null; menu = false">Cancel</v-btn>
          <v-btn text @click="menu = false" color="white">Ok</v-btn>
        </v-date-picker>
      </v-menu>

<!--      Template input-->
      <v-file-input
          label="Upload your template file"
          prepend-icon="mdi-upload"
          v-model="template"
      >
        <template v-slot:selection="{ file }">
          <v-chip
              small
              color="var(--btn-color)"
              class="white--text"
          >
            {{ file.name }}
          </v-chip>
        </template>
      </v-file-input>


<!--      Data files input-->
      <v-file-input
          label="Upload your data files"
          prepend-icon="mdi-upload"
          v-model="files"
          multiple
      >
        <template v-slot:selection="{ file }">
          <v-chip
              small
              color="var(--btn-color)"
              class="white--text"
          >
            {{ file.name }}
          </v-chip>
        </template>
      </v-file-input>


      <div class="d-flex flex-row bg-surface-variant">
        <div id="amount" style="font-weight: bold" class="ma-2 pa-2 mr-0 ml-0 pl-0">
          Amount of links:
          <v-tooltip color="white"  activator="#amount" bottom>
            <div style="color: black">The number of links returned for each sub-item<br/> while searching for information on the Internet</div>
          </v-tooltip>
        </div>
        <div class="ma-2 pa-2">{{amountOfLinks}}
        </div>
        <v-btn style="background-color: transparent!important;" class="ma-2 pa-2 elevation-0" v-on:click="decrement">
          <v-icon>mdi-minus</v-icon></v-btn>
        <v-btn style="font-weight: bold; background-color: transparent!important;" class="ma-2 pa-2 elevation-0" v-on:click="increment">
          <v-icon>mdi-plus</v-icon></v-btn>
      </div>


      <div class="d-flex flex-row bg-surface-variant">
        <div id="internet" style="font-weight: bold" class="ma-2 pa-2 mr-0 ml-0 pl-0">
          Search in the internet:
          <v-tooltip activator="#internet" color="white" bottom>
            <div style="color: black">Whether to use the Internet when searching for data</div>
          </v-tooltip>
        </div>
        <v-checkbox class="pt-0 ml-1" style="font-weight: bold" v-model="useInternet"></v-checkbox>
      </div>
<!--      <v-checkbox style="font-weight: bold"  label="Search in the internet" v-model="useInternet"></v-checkbox>-->

      <v-alert v-if="error" type="error">
        {{ error }}
      </v-alert>
      <v-btn @click="makeRequest" back>Analyse</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'SettingsComponent',
  data() {
    return {
      newUserSource: null,
      userSources: [],
      menu: false,
      dateRange: [],
      files: [],
      useInternet: false,
      template: null,
      amountOfLinks: 5,
      error: "",
      active: false,
      templates: [{name: 'First template', id: 1}, {name: 'Second template', id: 2}]
    };
  },
  beforeMount() {
    this.$root.$on("onRequestError", error => {
      console.log(error);
      this.error = error
    });
  },
  methods: {
    addUserSource: function () {
      if (this.newUserSource) {
        this.newUserSource = this.newUserSource.trim()
        if (this.newUserSource !== "") {
          this.userSources.push({value: this.newUserSource, index: this.userSources.length});
          this.newUserSource = '';
        }
      }
    },
    removeUserSource: function (index) {
      this.userSources.splice(index, 1);
    },
    makeRequest: function () {
      this.error = "";
      this.$root.$emit("onMakeRequest", this.userSources, this.amountOfLinks,
          this.dateRange, this.useInternet, this.template, this.files);
    },
    increment: function() {
      if (this.amountOfLinks < 15) {
        this.amountOfLinks++;
      }
    },
    decrement: function () {
      if (this.amountOfLinks > 1) {
        this.amountOfLinks--;
      }
    },
  },
  computed: {
  }
};
</script>

<style scoped>
</style>
