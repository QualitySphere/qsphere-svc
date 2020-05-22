<template>
  <el-menu
    :router="true"
    default-active="1-1"
    background-color="#EDEDED"
    text-color="#909399"
    active-text-color="#212529">
    <el-menu-item-group title="Dashboard" style="margin-top: 15px;">
      <el-menu-item index="1-1" route="/overview">
        <span style="margin-left: 15px;">Overview</span>
      </el-menu-item>
      <el-menu-item index="1-2" route="/project">
        <span style="margin-left: 15px;">Project</span>
      </el-menu-item>
      <el-menu-item index="1-3" route="/sprint">
        <span style="margin-left: 15px;">Sprint</span>
      </el-menu-item>
    </el-menu-item-group>
    <el-menu-item-group title="Portal" style="margin-top: 15px;">
      <el-menu-item index="2-1" :route="portal.jira" v-if="portal.jira">
        <span style="margin-left: 15px;">JIRA</span>
      </el-menu-item>
      <el-menu-item index="2-2" :route="portal.zentao" v-if="portal.zentao">
        <span style="margin-left: 15px;">Zentao</span>
      </el-menu-item>
      <el-menu-item index="2-3" :route="portal.bugzilla" v-if="portal.bugzilla">
        <span style="margin-left: 15px;">Bugzilla</span>
      </el-menu-item>
      <el-menu-item index="2-4" :route="portal.testlink" v-if="portal.testlink">
        <span style="margin-left: 15px;">TestLink</span>
      </el-menu-item>
    </el-menu-item-group>
  </el-menu>
</template>

<script>
import trackerSvc from '@/services/trackerSvc'
export default {
  data () {
    return {
      tabPosition: 'left',
      portal: {
        jira: '',
        zentao: '',
        bugzilla: '',
        testlink: ''
      }
    }
  },
  methods: {
    generatePortal () {
      trackerSvc.listTracker()
        .then((response) => {
          console.log(response.data.detail.results)
          var trackers = response.data.detail.results
          var i
          for (i in trackers) {
            if (trackers[i].type === 'jira') {
              console.log(trackers[i].info.host)
              this.portal.jira = trackers[i].info.host
            }
            if (trackers[i].type === 'bugzilla') {
              this.portal.bugzilla = trackers[i].info.host
            }
            if (trackers[i].type === 'zentao') {
              this.portal.zentao = trackers[i].info.host
            }
            if (trackers[i].type === 'testlink') {
              this.portal.testlink = trackers[i].info.host
            }
            console.log((this.portal))
          }
        })
        .catch((error) => {
          this.$message.error(error)
        })
    }
  },
  mounted: function () {
    this.generatePortal()
  }
}
</script>

<style scoped lang="scss">

  .el-menu {
    height: 100%;
    text-align: left;
  }

  .el-menu-item {
    font-size: 16px;
  }

</style>
