<template>
    <div :class="className"
        @mouseover="displayTeamName()"
        @click="displayTeamName()">
        <!-- @mouseleave="isHover = false"> -->
        <!-- @click="wasClick=true, displayTeamName()"> -->
        <!-- {{ rank.espn_team.team_name }} -->

        <img v-bind:src="team_obj.logo_url" v-bind:alt="team_obj.team_name" >
        <div class="team-name-modal" v-if="showName">
            <div class="name-text">
                {{team_obj.team_name}}
            </div>
        </div>
    </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
export default {
    name: 'TeamName',
    props: {
        team_obj: Object,
        className: String
    },
    setup() {
        const isHover = ref(false)
        const showName = ref(false)
        const wasClick = ref(false)

        function displayTeamName() {
            console.log('wasClick' + wasClick.value)
            console.log('isHover' + isHover.value)
            console.log('showName' + showName.value)
            showName.value = true
             setTimeout(() => {
                    showName.value = false
                    wasClick.value = false
                }, 3000)



            // if(wasClick.value===true) {
            //     showName.value = true
            //     setTimeout(() => {
            //         showName.value = false
            //         wasClick.value = false
            //     }, 3000)

            // } else if(isHover.value===true) {
            //     showName.value= true
            // } else if(isHover.value===false) {
            //     showName.value= false
            // }

        }

        watch(()=>isHover, (isHover, prevIsHover) => {
            console.log('watching is hover' + isHover.value)
            displayTeamName()
        })

        return {
            isHover,
            wasClick,
            showName,
            displayTeamName
        }
        
    },
}
</script>


<style>

.team-name-modal {
    font-size: 9px;
    position: absolute;
    z-index: 1000;
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    top:0;
    left:0;
}

.team-name-modal > .name-text{
    text-align: center;
    height: max-content;
    width: max-content;
    background-color: rgba(0, 0, 0, 0.8);
    border-radius: 5px;
    box-shadow: 0px 5px 5px black;
    color: white;
    padding: 5px 5px 5px 5px;
}
</style>