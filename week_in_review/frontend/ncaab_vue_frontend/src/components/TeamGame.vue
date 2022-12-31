<template>
    <div class="td-game-wrapper" :class="{ is_win: game.is_win, is_loss: (!game.is_win && game.final_score) }">
        <div class="game-data" v-if="game.week_number !== null">
            <div class="game-date">
                {{ formatDate(game.game_date) }}
            </div>
            <div class="game-location">
                <div v-if="game.is_home">vs</div>
                <div v-else-if="game.is_neutral_court">vs*</div>
                <div v-else>@</div>
            </div>
            <div v-if="game.opponent_week_ranking" class="opponent-ranking">{{ game.opponent_week_ranking }}</div>
            <TeamName :team_obj="game.opponent_espn_team" className="opponent-name" />
            <!-- <div class="opponent-name">
                {{ game.opponent_espn_team.team_name }}
                <img v-bind:src="game.opponent_espn_team.logo_url" v-bind:alt="game.opponent_espn_team.team_name">
            </div> -->
            <div class="final-score">
                <div v-if="(game.is_win === true)" class="score">
                    <div class="left-score">
                        {{ game.final_score }}
                    </div>
                    <!-- <div class="sep" v-if="game.is_home===true" >vs</div>
                    <div class="sep" v-else-if="game.is_neutral_court===true" >vs*</div>
                    <div class="sep" v-else>@</div>  -->
                    <div class="sep">-</div>

                    <div class="right-score">
                        {{ game.opponent_final_score }}
                    </div>
                </div>
                <div v-else-if="(game.is_win === false && game.cancelled_or_postponed === false)" class="score">
                    <div class="left-score">
                        {{ game.opponent_final_score }}
                    </div>
                    <div class="sep">-</div>
                    <div class="right-score">
                        {{ game.final_score }}
                    </div>
                </div>
                <div v-else-if="(game.is_win === false && game.cancelled_or_postponed === true)" class="unplayed_info">
                    PPD
                </div>
                <div v-else-if="(!game.cancelled_or_postponed && game.game_time)" class="unplayed_info">{{
        game.game_time
                    }}</div>
            </div>
        </div>
    </div>
</template>


<script>
// import { ref, onMounted, watch, computed } from 'vue'
import TeamName from "@/components/TeamName.vue";
export default {
    name: 'TeamGame',
    props: {
        game: Object
    },
    components: {
        TeamName,
    },
    setup() {

        function formatDate(dateStr) {
            if (typeof dateStr === 'string' || dateStr instanceof String) {
                const date = new Date(dateStr);
                // Then specify how you want your dates to be formatted
                // var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
                var parts = dateStr.split('-');
                //new Intl.DateTimeFormat('default', {dateStyle: 'long'}).format(date);
                // return months[parts[1] - 1] + ' ' + Number(parts[2]) 
                return parts[1] + '-' + parts[2]
            }
            else {
                return ''
            }


        }

        // expose to template and other options API hooks
        return {
            formatDate
        }
    }
}

</script>

