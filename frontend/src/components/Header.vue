<template>
  <v-app-bar flat class="bar" color="#09002B">
    <v-toolbar-title>AI-Powered Data Analysis</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-toolbar-items>
      <v-btn id="menu">
        Templates
      </v-btn>
      <v-menu activator="#menu" right>
        <v-list color="primary">
          <v-list-item
              v-for="(template, id) in templates" :key="id"
              @click="download(template.id)"
          >
            <v-list-item-title >{{template.name}}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-btn >Contacts</v-btn>
    </v-toolbar-items>
  </v-app-bar>
</template>

<script>
export default {
  name: "HeaderComponent",
  data() {
    return {
      templates: [{name: 'Шаблон анализа конкурентов', id: 1}, {name: 'Анализ компании "Газпром"', id: 2}]
    };
  },
  methods: {
    download: function (id) {
      this.$root.$emit("onDownloadTemplate", id);
    }
  }
};
</script>

<style scoped>
.v-btn {
  background-color: var(--top-color)!important;
}
/* Add any custom styles here */
</style>
