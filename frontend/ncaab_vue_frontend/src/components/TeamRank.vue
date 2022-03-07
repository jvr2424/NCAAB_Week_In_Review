<template>
    <td>
        <div class="team-info">
            <div class="team-rank">
            {{ rank.ranking }}
            </div>
            
            <TeamName :team_obj="rank.espn_team" className="team-name"/>
            
        </div>
    </td>
    <td v-for="(game) in rank.schedule" :key="game.game_date" >
        <TeamGame :game="game"/>
    </td>
</template>

<script>
import TeamGame from "@/components/TeamGame.vue";
import TeamName from "@/components/TeamName.vue";
// import { ref, onMounted, watch, computed } from 'vue'
export default {
  name: 'TeamRank',
  components: {
    TeamGame,
    TeamName,
  },
    props: {
        rank: Object
    },
  setup() {
 
    // expose to template and other options API hooks
    return {
      
    }
  }
}
</script>

