<template>
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

:root{

  --color-main00:#f5f5f5;
  --color-main01:#cbe5e7;
  --color-main02:#7fcec3;
  --color-main03:#289482;
  --color-main04:#165e52;

}

*{
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

header{
  background-color: var(--color-main01);
  padding: 14px 0;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-start;

}

section#dataEscolhida{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.home-view{
  position: relative;
}

footer{
  position: fixed;
  bottom: 0;
  width: 100vw;
  background-color: var(--color-main01);
  padding: 3px 0;
}

</style>
