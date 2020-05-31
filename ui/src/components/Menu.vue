<template>
  <el-menu
    :router="true"
    default-active="1"
    background-color="#EDEDED"
    text-color="#909399"
    active-text-color="#212529">
    <el-menu-item-group title="Dashboard" style="margin-top: 15px;">
      <el-menu-item index="1" route="/overview">
        <i class="el-icon-data-board"></i><span>Overview</span>
      </el-menu-item>
      <el-menu-item index="2" route="/project">
        <i class="el-icon-data-line"></i><span>Project</span>
      </el-menu-item>
      <el-menu-item index="3" route="/sprint">
        <i class="el-icon-data-analysis"></i><span>Sprint</span>
      </el-menu-item>
    </el-menu-item-group>
    <el-menu-item-group title="Portal" style="margin-top: 15px;">
      <el-menu-item v-for="item in portal" :key="item.value">
        <div @click="openTracker(item.value)">
          <i class="el-icon-position"></i>
          <span>{{ item.key }}</span>
        </div>
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
      portal: []
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
              this.portal.push({
                key: 'Jira',
                value: trackers[i].info.host
              })
            }
            if (trackers[i].type === 'bugzilla') {
              console.log(trackers[i].info.host)
              this.portal.push({
                key: 'Bugzilla',
                value: trackers[i].info.host
              })
            }
            if (trackers[i].type === 'zentao') {
              console.log(trackers[i].info.host)
              this.portal.push({
                key: 'Zentao',
                value: trackers[i].info.host
              })
            }
            if (trackers[i].type === 'testlink') {
              console.log(trackers[i].info.host)
              this.portal.push({
                key: 'TestLink',
                value: trackers[i].info.host
              })
            }
            console.log((this.portal))
          }
        })
        .catch((error) => {
          this.$message.error(error)
        })
    },
    openTracker (url) {
      window.open(url)
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
