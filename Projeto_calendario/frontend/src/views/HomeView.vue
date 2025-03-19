<template>
  <div class="home-view">
    
    <header>
      <section id="escolhaData">
        <div id="mesEscolha">
          <ul>
            <li @click="procurarEventosMes(1, this.anoSelecionado)">Jan</li>
            <li @click="procurarEventosMes(2, this.anoSelecionado)">Fev</li>
            <li @click="procurarEventosMes(3, this.anoSelecionado)">Mar</li>
            <li @click="procurarEventosMes(4, this.anoSelecionado)">Abr</li>
            <li @click="procurarEventosMes(5, this.anoSelecionado)">Mai</li>
            <li @click="procurarEventosMes(6, this.anoSelecionado)">Jun</li>
            <li @click="procurarEventosMes(7, this.anoSelecionado)">Jul</li>
            <li @click="procurarEventosMes(8, this.anoSelecionado)">Ago</li>
            <li @click="procurarEventosMes(9, this.anoSelecionado)">Set</li>
            <li @click="procurarEventosMes(10, this.anoSelecionado)">Out</li>
            <li @click="procurarEventosMes(11, this.anoSelecionado)">Nov</li>
            <li @click="procurarEventosMes(12, this.anoSelecionado)">Dez</li>
          </ul>
        </div>
        <div id="anoEscolha">
          <!-- loop para gerar os próximos 3 anos -->
          <ul>
            <li v-for="numero in 3" :key="numero" :id="`${this.anoAtual + numero}`" @click="procurarEventosMes(this.mesSelecionado, (this.anoAtual - 1 ) + numero)">{{(this.anoAtual - 1 ) + numero}}</li>
          </ul>
        </div>
      </section>

      <section id="dataEscolhida">
        <h1>{{this.mesSelecionadoString}}</h1>
        <h1>{{this.anoSelecionado}}</h1>
      </section>

      <aside>
        <p>Calendário</p>
      </aside>

    </header>

    <main>

      <section id="calendario">

        <!-- display grid de 7 colunas -->
        <div id="diasMes">
          <ul>
            <li class="dia" v-for="numero in this.contagemDia" :key="numero" @click="procurarEventosDia(numero, this.mesSelecionado)">
              {{numero}}
            </li>
          </ul>

          <div v-if="mostrarDia" class="dia-card">

            <button @click="ocultarCard()">fechar</button>
            <h2>Eventos no dia {{this.diaSelecionado}} de {{this.mesSelecionadoString}} de {{this.anoSelecionado}}</h2>
            <section v-for="evento in eventos" :key="evento.id">
              <h1>{{evento.descricao}}</h1>
              <h1>{{evento.data}}</h1>
              <h1>{{evento.cor}}</h1>
              <button>Editar</button>
              <button>Deletar</button>
            </section>
            <h1>{{this.diaSelecionado}}</h1>

          </div>

          <!-- formulario de resgistro e edição de evento -->
          <div v-if="mostrarFormulario" class="formulario">

            <form enctype="multipart/form-data" @submit="isRegister == true ? registerEvento() : atualizarEvento()">
            
              <div class="input-container">
                <label for="descricao">Descrição do evento:</label>
                <input type="text" name="descricao" id="descricao" v-model="descricao" placeholder="Descrição do evento" required>
              </div>

              <div class="input-container" v-if="sempre == false">
                <label for="quant">Por quantos anos se repete?</label>
                <input type="number" name="quant" id="quant" v-model="quant" placeholder="Quantidade de anos" required>
              </div>

              <input type="hidden" name="data" id="data" v-model="data">
              <input type="hidden" name="ultimaData" id="ultimaData" v-model="ultima_data">

              <div class="input-container">
                <label for="sempre">Evento sempre se repete?</label>
                <input type="checkbox" name="sempre" id="sempre" v-model="sempre">
              </div>

              <div class="input-container">
                <input type="color" name="cor" id="cor" v-model="cor" required>
              </div>

              <div class="input-container">
                <button type="submit">{{isRegister == true ? "Cadastrar" : "Atualizar"}}</button>
              </div>

            </form>

          </div>

        </div>

      </section>

    </main>

    <footer>

      <p>Ciências da Computação 2024.2</p>

    </footer>


  </div>
</template>

<script>

/* 

gerar estilos do calendario, card e formulario
preparar pra receber a API

*/

export default {
  name: 'HomeView',
  components: {
    
  },
  data(){
    return {

      //variáveis de data:
      anoAtual: 2025,
      mesAtual: 3,
      diaAtual: 0,
      contagemDia: 0,
      anoSelecionado: 0,
      mesSelecionado:0,
      mesSelecionadoString: null,
      diaSelecionado: 0,
      eventos:[
        {id: 1, descricao: "Evento 1", data: "2025-03-01", cor: "azul"},
        {id: 2, descricao: "Evento 2", data: "2025-03-01", cor: "vermelho"},  
        {id: 3, descricao: "Evento 3", data: "2025-03-01", cor: "verde"},
      ],


      //variáveis de formulário:
      descricao: null,
      data: null,
      ultima_data: null,
      sempre: true,
      cor: null,
      isRegister: true,
      quant: 0,

      // variaveis de controle de exibição:
      mostrarFormulario: true,
      mostrarDia: false,

    }
  },
  created(){

    //coletar data atual
    var data = new Date()
    this.anoAtual = data.getFullYear()
    this.mesAtual = data.getMonth() + 1
    this.diaAtual = data.getDate()
    this.contagemDia = data.getDay()
    this.anoSelecionado = this.anoAtual
    this.mesSelecionado = this.mesAtual
    this.mesSelecionadoString = this.mesString(this.mesSelecionado)
    this.diaSelecionado = this.diaAtual
    this.contagemDia = new Date(this.anoAtual, this.mesSelecionado, 0).getDate()

  },
  methods:{

    //procurar eventos por mes com base na escolha do usuário
    procurarEventosMes(mes, ano){

      this.contagemDia = new Date(ano, mes, 0).getDate()
      this.anoSelecionado = ano
      this.mesSelecionado = mes
      this.mesSelecionadoString = this.mesString(mes)
      console.log(`${ano} ${mes} dias: ${this.contagemDia}`)

    },

    //procurar eventos por dia com base na escolha do usuário
    procurarEventosDia(dia, mes){

      this.diaSelecionado = dia
      this.mesSelecionado = mes
      this.mostrarDia = true
      console.log(`${dia} ${mes}`)

    },

    ocultarCard(){
      this.mostrarDia = false
    },

    // coleta o numero do mes e retorna o nome do mes por extenso
    mesString(mesNumero){
        switch (mesNumero) {
        case 1:
          return "Janeiro"
        case 2:
          return "Fevereiro"
        case 3:
          return "Março"
        case 4:
          return "Abril" 
        case 5:
          return "Maio"
        case 6:
          return "Junho"
        case 7:
          return "Julho" 
        case 8:
          return "Agosto"
        case 9:
          return "Setembro"
        case 10:
          return "Outubro"
        case 11:
          return "Novembro"  
        case 12:
          return "Dezembro"
      }
    }

  }
}
</script>
