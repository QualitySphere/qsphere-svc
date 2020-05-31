<template>
  <div id="app">
    <el-container style="height: 1024px">
      <el-header>
        <Nav/>
      </el-header>
      <el-container>
        <el-aside width="150px">
          <Menu/>
        </el-aside>
        <el-main>
          <router-view/>
        </el-main>
      </el-container>
      <el-footer>
        <Footer/>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import Nav from '@/components/Nav.vue'
import Menu from '@/components/Menu.vue'
import Footer from '@/components/Footer.vue'

export default {
  components: {
    Nav,
    Menu,
    Footer
  }
}
</script>

<style lang="scss">
  *{
    box-sizing: border-box;
  }

  .el-header {
    background-color: #212529;
    text-align: right;
  }

  .el-aside .el-main {
    background-color: #EDEDED;
  }

  .el-footer {
    background-color: #212529;
  }

#app {
  font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,"Noto Sans",sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol","Noto Color Emoji";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #212529;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>
