<template>
  <el-tabs type="border-card" style="height: 100%">
    <el-tab-pane>
      <span slot="label"><i class="el-icon-connection"></i> Tracker</span>
      <Tracker/>
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label"><i class="el-icon-menu"></i> Project</span>
      <Project/>
    </el-tab-pane>
    <el-tab-pane>
      <span slot="label"><i class="el-icon-s-grid"></i> Sprint</span>
      <Sprint/>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
import Tracker from '@/components/Tracker.vue'
import Project from '@/components/Project.vue'
import Sprint from '@/components/Sprint.vue'
export default {
  components: {
    Tracker,
    Project,
    Sprint
  }
}
</script>
