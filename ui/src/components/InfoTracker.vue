<template>
  <div>
    <div v-if="this.$route.path.id" class="warning">
      check and EDIT tracker info
    </div>
    <div v-else>
      <div v-if="this.$route.path.type == 'jira'" class="primary">
        Hi, do you wanna ADD new JIRA tracker
      </div>
      <div v-if="this.$route.path.type == 'zentao'" class="primary">
        Hi, do you wanna ADD new ZENTAO tracker
      </div>
      <div v-if="this.$route.path.type == 'bugzilla'" class="primary">
        Hi, do you wanna ADD new BUGZILLA tracker
      </div>
      <div v-if="this.$route.path.type == 'testlink'" class="primary">
        Hi, do you wanna ADD new TESTLINK tracker
      </div>
    </div>
  </div>
</template>
