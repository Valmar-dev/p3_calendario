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

button{
  border: none;
  outline: 0;

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

.background-card{
  position: fixed;
  top: 0;
  z-index: 1000;
  width: 100vw;
  height: 100vh;
  background-color: var(--color-main00);;
  opacity: 0.7;
}

.card{
  position: fixed;
  bottom: 0;
  z-index: 1001;
  background-color: var(--color-main02);;
  width: 100vw;
  padding: 25px 0 0 0;
  border-radius: 40px 40px 0 0;
  opacity: 1;
  border: none;
  outline: none;
  user-select: none;
}

.bar{
  position: absolute;
  top: 10px;
  right: 50vw;
  transform: translateX(50%) ;
  width: 30%;
  height: 10px;
  background-color: var(--color-main04);
  border-radius: 10px;
}
  
.bar:active{
  background-color: var(--color-main03);
}

.botao-fechar{
  position: absolute;
  top: 0;
  right: 0;
  background-color: var(--color-main04);
  color:#fff;
  border-radius: 50%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 37px;
  height: 37px;
  fill: var(--color-main01);
}

.botao-fechar:active{
  scale: 0.9;
}

.botao-fechar:hover{
  cursor: pointer;
  background-color: var(--color-main03);
}


footer{
  position: fixed;
  bottom: 0;
  width: 100vw;
  background-color: var(--color-main01);
  padding: 3px 0;
}

</style>
