<template>
  <div class="HomeMonthView">
    
    <header>
      <section id="ChoiceDate">
        <div id="MonthChoide">
          <ul>
            <li>Jan</li>
            <li>Fev</li>
            <li>Mar</li>
            <li>Abr</li>
            <li>Mai</li>
            <li>Jun</li>
            <li>Jul</li>
            <li>Ago</li>
            <li>Set</li>
            <li>Out</li>
            <li>Nov</li>
            <li>Dez</li>
          </ul>
        </div>
        <div id="YearDate">
          <ul><!-- fazer loop para a cada 5 anos a frente do atual -->
      
          </ul>
        </div>
      </section>

      <section id="MontSelected">
        <h1>Março</h1>
        <h1>2025</h1>
      </section>

      <aside>
        <p>Calendário</p>
      </aside>

    </header>


  </div>
</template>

<script>


export default {
  name: 'HomeView',
  components: {
    
  }
}
</script>
