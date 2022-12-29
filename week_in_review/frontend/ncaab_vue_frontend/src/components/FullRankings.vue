<script>
import TeamRank from "@/components/TeamRank.vue";
import { ref, onMounted, watch, computed } from 'vue'


export default {
  name: 'FullRankings',
  components: {
    TeamRank,
  },
  setup() {
    const api_data = ref({}) 
    const all_weeks = ref({})
    const selected_week = ref({})
    

    function formatDate(dateStr) {
      const date = new Date(dateStr);
                // Then specify how you want your dates to be formatted
      // var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      var parts = dateStr.split('-');
      //new Intl.DateTimeFormat('default', {dateStyle: 'long'}).format(date);
      // return months[parts[1] - 1] + ' ' + Number(parts[2]) 
      return parts[1] + '-' + parts[2]
       

    }

    watch(() => selected_week,
      (selected_week, prev_selected_week) => {
        getFullWeek(selected_week.value)
        /* ... */
      }
    )

    function getFullWeek(weekNum){
      fetch(`${import.meta.env.VITE_API_BASE_URI}/weeks_full/${weekNum}`)
      // `http://10.8.29.182:8000/weeks_full/${weekNum}`
        .then(response => response.json())
        .then(data => {
          api_data.value = data
          console.log(data)
          })
    }

    function getWeeksList(){
      //http://127.0.0.1:8000/weeks/
      // console.log(import.meta.env.VITE_API_BASE_URI)
      fetch(`${import.meta.env.VITE_API_BASE_URI}/weeks/`)
        .then(response => response.json())
        .then(data => {
          all_weeks.value = data
          console.log(data)
          selected_week.value = data.filter(week => week.is_current_week).map((week)=>  week.week_number)[0]
          getFullWeek(selected_week.value)
          
          })
    }
    
    // computed(() =>


    getWeeksList()

    // onMounted(()=>{
      
    // })

    // expose to template and other options API hooks
    return {
      api_data,
      formatDate,
      selected_week,
      all_weeks,
      getFullWeek

    }
  }
}
</script>
 
<template>
  <div class="wrapper">
    <!-- add dropdown to select week -->
    <div class="select-week">
      <div class="label">Select Week:</div>
      <select v-model="selected_week" @change="getFullWeek(selected_week)">
        <option v-for="week in all_weeks" v-bind:key="week.week_number" v-bind:value="week.week_number">{{week.week_number}}</option>
      </select>
    </div>
    <table>
      <thead>
          <tr>
            <td>RK</td>
            <td>Games</td>
          </tr>
      </thead>
      <tbody>
        <tr v-for="(rank) in api_data.rankings" :key="rank.ranking">
          <TeamRank :rank="rank"/>
          
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style>
*{
  box-sizing: border-box;
  }

.wrapper{
  width: 75%;
  margin: 0 auto;
  display: flex;
  flex-direction: column;

}
.wrapper .select-week {
  margin:0 auto 15px;
  display: flex;
  gap:45px;
  
  
}

table {
  table-layout: fixed;
  border-collapse: collapse;
  margin:0 auto;
}

tr {
  height: 20px;
  position: relative;
  border-bottom: 1px solid black;
}


td {
  width:80px;
  position: relative;
  /* display: inline; */
}

tr>td:nth-child(1){
  border-spacing: 0;
  border-right: 1px solid black;
}
.td-game-wrapper { 
    position: absolute;
    height: 100%;
    width: 100%;
    top:0;
    left:0;
  }

.team-info {
  position: relative;
  /* height: 100%; */
  
  display: grid;
  grid-template-columns: 15% 85%;
  grid-template-rows: 50% 50%;

}

.game-date {
  grid-row-start: 1;
  grid-row-end: 2;
  grid-column-start: 1;
  grid-column-end: 2;
  font-size: 6px;
  padding-left:1px;
  color: gray;
  /* border-right: 1px solid black;
  border-left: 1px solid black;
  border-bottom: 1px solid black; */
}  
.team-rank {
  grid-row-start: 1;
  grid-row-end: 3;
  grid-column-start: 1;
  grid-column-end: 2;
  text-align: center;
}
.team-name {
  margin-left: 9px;
  grid-row-start: 1;
  grid-row-end: 3;
  grid-column-start: 2;
  grid-column-end: 3;

}



.game-data {
  width:100%; 
  height: 100%;
  /* padding:10px; */
  display:grid;
  grid-template-rows: 30% 40% 30%;
  grid-template-columns: 30% 40% 30%;
}

.game-location {
  grid-row-start: 2;
  grid-row-end: 3;
  grid-column-start: 1;
  grid-column-end: 2;
}

.game-location > div {
  height: 100%;
  display: flex;
  align-items: center;
  font-size: 6px;
  color: gray;
  margin-left: 2px;

}

.opponent-ranking {
  grid-row-start: 1;
  grid-row-end: 2;
  grid-column-start: 3;
  grid-column-end: 4;
  font-size: 7px;
  color: rgb(73, 73, 73);
  margin-right: 3px;
  text-align: right;
}

.opponent-name {
  position: relative;
  grid-row-start: 1;
  grid-row-end: 4;
  grid-column-start: 1;
  grid-column-end: 4;
  display: flex;
  align-items: center;
  justify-content: center;
}

.team-name,
.team-rank {
  display:inline;
}
.team-name >img {
  height: 20px;
  width: 20px;
  

}

.opponent-name > img {
  height: 20px;
  width: 20px;
  text-align: center;
  opacity: 0.55;
  font-size: 9px;
}


.final-score {
  grid-row-start: 2;
  grid-row-end: 3;
  grid-column-start: 1;
  grid-column-end: 4;
  font-size: 9px;
  /* width: 100%; */
  display: grid;
  grid-template-columns: 33% 34% 33%;
}

.final-score > .score {
  grid-column-start: 1;
  grid-column-end: 4;
  display: grid;
  grid-template-columns: 33% 34% 33%;
}

.final-score >  .score > .left-score { 
  grid-column-start: 1;
  grid-column-end: 2;
  text-align: right;

}

.final-score > .score > .sep { 
  grid-column-start: 2;
  grid-column-end: 3;
  text-align: center;

}

.final-score > .right-score { 
  grid-column-start: 3;
  grid-column-end: 4;
  text-align: left;
}


.final-score > .unplayed_info {
  grid-column-start: 3;
  grid-column-end: 4;
  text-align: center;
  color:grey;
  font-size: 6px;
  margin-top: 10px;
  width: max-content;
}

.is_win{
  /* background-color: #cfffc1; */
  background-color: #c1fec1
}

.is_loss{
  /* background-color: #ffc8c8; */
  background-color: #fec1c1

}

</style>
