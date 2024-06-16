<template>
  <v-container class="settings">
    <!-- Displaying existing settings -->
    <v-list color=var(--top-color) dense style="max-height: 180px"
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


      <v-checkbox label="Search in the internet" v-model="useInternet"></v-checkbox>

      <v-alert v-if="error" type="error">
        {{ error }}
      </v-alert>
      <v-btn @click="makeRequest" back>Analyse</v-btn>
    </v-form>
  </v-container>
</template>

<script>
// import format from 'date-fns/format'
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
      error: "",
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
      this.$root.$emit("onMakeRequest", this.userSources, this.dateRange, this.useInternet, this.template, this.files);
    },
  },
  computed: {
  }
};
</script>

<style scoped>
</style>
