/* eslint-disable */
<template>   
    <div>
        <v-container
        class="fill-height"
        fluid>
            <v-fade-transition mode="out-in">
                <v-row>                
                    <v-col v-for="poke in pokemons" :key="poke.name" cols="2">
                        <v-card hover>

                            <v-img
                            v-bind:src="getImage(poke.url)"
                            max-height="150"
                            contain
                            class="background-img-card">
                                <template v-slot:placeholder>
                                    <v-row
                                        class="fill-height ma-0"
                                        align="center"
                                        justify="center">
                                        
                                        <v-progress-circular
                                        indeterminate
                                        color="cyan lighten-5"
                                        ></v-progress-circular>
                                    </v-row>
                                </template>
                            </v-img>

                            <v-card-title class="text-h6">
                                {{poke.name | capitalize }}
                            </v-card-title>

                            <v-card-actions>
                                <v-row justify="space-around">
                                    <v-col cols="auto">
                                        <v-dialog
                                            transition="dialog-bottom-transition"
                                            max-width="600" @input="">
                                            <template v-slot:activator="{ on, attrs }">
                                                <v-btn color="primary"
                                                    v-bind="attrs"
                                                    v-on="on"
                                                    @click="getPokeData(poke.name)">Info</v-btn>
                                            </template>
                                            
                                            <!-- Dialog popup -->
                                            <template v-slot:default="dialog">
                                                <v-card>
                                                    <!-- toolbar titles -->
                                                    <v-toolbar color="red darken-2">
                                                        <v-img class="mr-3" v-bind:src="getImage(poke.url)" max-height="70px" max-width="70px"></v-img>
                                                        <v-toolbar-title>{{ poke.name | capitalize }}</v-toolbar-title>
                                                        <!-- template tabs -->
                                                        <template v-slot:extension>
                                                            <v-tabs color="white" v-model="tab" align-with-title show-arrows>
                                                                <v-tabs-slider color="green accent-3"></v-tabs-slider>
                                                                <v-tab color="white" v-for="tab in tabs" :key="tab">
                                                                    {{ tab }}
                                                                </v-tab>
                                                            </v-tabs>
                                                        </template>
                                                        <!-- template tabs -->
                                                    </v-toolbar>
                                                    <!-- toolbar titles -->

                                                    <!-- tabs content -->
                                                    <v-tabs-items v-model="tab">
                                                        <!--<v-tab-item v-for="tab in info">
                                                            <v-card flat>
                                                                <v-card-text v-text=""></v-card-text>
                                                                <!-- v-text el texto a mostrar --
                                                                <v-simple-table fixed-header height="300px">
                                                                    <template v-slot:default>
                                                                        <thead>                                                                            
                                                                            <th class="text-center">
                                                                               {{ tab | capitalize }}
                                                                            </th>
                                                                            <th class="text-center">
                                                                                Value
                                                                            </th>
                                                                            </tr>
                                                                        </thead>
                                                                        <tbody>
                                                                            <!--<tr v-for="data in pokemonData">
                                                                                <td>{{ pokemonData }}</td>
                                                                            </tr>--
                                                                            <tr>
                                                                                <td>{{pokemonData.abilities[0]['ability'].name}}</td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </template>
                                                                </v-simple-table>
                                                            </v-card>
                                                        </v-tab-item>-->
                                                        
                                                        <!-- Estadisticas -->
                                                        <v-tab-item>
                                                            <v-card flat class="pa-3">
                                                                <v-card-text>
                                                                    <!-- Loader + contenido -->
                                                                    <p class="font-weight-bold text-left text-subtitle-1">Acerca de este Pokemon</p>
                                                                    <v-sheet>
                                                                        <v-skeleton-loader :loading="loading" :transition="transition" height="94" type="paragraph" >
                                                                            <template>
                                                                                <div>
                                                                                    <div class="text--primary text-justify">
                                                                                        {{ pokemonData.descripcion}}                                                                        
                                                                                    </div>

                                                                                    <p class="font-weight-bold text-left text-subtitle-1">Tipo</p>
                                                                                    <div class="text--primary text-left">
                                                                                        <ul>
                                                                                            <li style="display: inline; list-style-type: none;" v-for="(stat, index) in pokemonData.types">                                                                                        
                                                                                                <v-chip
                                                                                                class="ma-2"
                                                                                                v-bind:color=chip_colors[index]
                                                                                                text-color="white">
                                                                                                    {{stat.name}}                                                                                
                                                                                                </v-chip> 
                                                                                            </li>
                                                                                        </ul>
                                                                                    </div>

                                                                                    <p class="font-weight-bold text-left text-subtitle-1">Altura</p>
                                                                                    <p class="text--primary text-left" >
                                                                                        {{ height(pokemonData.height) }} mt
                                                                                    </p>

                                                                                    <p class="font-weight-bold text-left text-subtitle-1">Peso</p>
                                                                                    <p class="text--primary text-left" >
                                                                                        {{ weight(pokemonData.weight)}} kg
                                                                                    </p>
                                                                                </div>
                                                                            </template>
                                                                        </v-skeleton-loader>
                                                                    </v-sheet>
                                                                    
                                                                    <p class="font-weight-bold text-left text-subtitle-1">Estadísticas</p>
                                                                    <v-sheet>                                                                        
                                                                        <v-skeleton-loader :loading="loading" :transition="transition" height="94" type="table">
                                                                            <v-simple-table fixed-header>
                                                                                <template v-slot:default>
                                                                                    <thead>
                                                                                        <tr>
                                                                                            <th class="text-left">
                                                                                                Stat
                                                                                            </th>
                                                                                            <th class="text-center">
                                                                                                Valor
                                                                                            </th>
                                                                                        </tr>
                                                                                    </thead>
                                                                                    <tbody>
                                                                                        <tr v-for="(stat, index) in pokemonData.stats">
                                                                                            <td class="text-left">
                                                                                                <v-chip
                                                                                                class="ma-2"
                                                                                                v-bind:color=chip_colors[index]
                                                                                                text-color="white">
                                                                                                    {{stat.name | capiReplace}}
                                                                                                    {{pokemonData.id}}
                                                                                                </v-chip>                                                                                        
                                                                                            </td>
                                                                                            <td class="text-center">
                                                                                                <v-chip
                                                                                                class="ma-2"
                                                                                                v-bind:color=chip_colors[index]
                                                                                                text-color="white">
                                                                                                    <strong>{{stat.value}}</strong>
                                                                                                </v-chip>
                                                                                            </td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </template>
                                                                            </v-simple-table>
                                                                        </v-skeleton-loader>
                                                                    </v-sheet>
                                                                    <!-- Loader + contenido -->

                                                                    
                                                                </v-card-text>
                                                            </v-card>
                                                        </v-tab-item>
                                                        <!-- Estadisticas -->

                                                        <!-- Habilidades -->
                                                        <v-tab-item>
                                                            <v-card flat>
                                                                <v-card-text>                                                                    
                                                                    <v-list class="text-left" two-line>
                                                                        <v-list-item-group class="pink--text">
                                                                            <template v-for="(ab, index) in pokemonData.abilities">
                                                                                <!-- Loader + contenido -->
                                                                                <v-sheet>
                                                                                    <v-skeleton-loader
                                                                                    :loading="loading"
                                                                                    :transition="transition"
                                                                                    height="94"
                                                                                    type="list-item-two-line" >
                                                                                    <v-list-item :key="ab.name">
                                                                                        <template>
                                                                                            <v-list-item-content>
                                                                                                <v-list-item-title> {{ab.name| capiReplace}} </v-list-item-title>
                                                                                                <v-list-item-content class="text--primary">{{ab.desc}}</v-list-item-content>
                                                                                            </v-list-item-content>                                                                                
                                                                                        </template>
                                                                                    </v-list-item>
                                                                                    </v-skeleton-loader>
                                                                                </v-sheet>
                                                                                <!-- Loader + contenido -->
                                                                                <v-divider></v-divider>
                                                                            </template>
                                                                        </v-list-item-group>
                                                                    </v-list>
                                                                </v-card-text>
                                                            </v-card>
                                                        </v-tab-item>
                                                        <!-- Habilidades -->
                                                        
                                                        <!-- movimientos -->
                                                        <v-tab-item>
                                                            <v-card flat>
                                                                <v-card-text>
                                                                    <v-list class="text-left" two-line>
                                                                        <v-list-item-group class="pink--text">
                                                                            <template v-for="(move, index) in pokemonData.moves">
                                                                                <!-- Loader + contenido -->
                                                                                <v-sheet>
                                                                                    <v-skeleton-loader
                                                                                    :loading="loading"
                                                                                    :transition="transition"
                                                                                    height="94"
                                                                                    type="list-item-two-line" >
                                                                                    <v-list-item :key="move.name">
                                                                                        <template>
                                                                                            <v-list-item-content>
                                                                                                <v-list-item-title> {{move.name| capiReplace}} </v-list-item-title>
                                                                                                <v-list-item-content class="text--primary">{{move.desc}}</v-list-item-content>
                                                                                            </v-list-item-content>                                                                                
                                                                                        </template>
                                                                                    </v-list-item>
                                                                                    </v-skeleton-loader>
                                                                                </v-sheet>
                                                                                <!-- Loader + contenido -->
                                                                                <v-divider></v-divider>
                                                                            </template>
                                                                        </v-list-item-group>
                                                                    </v-list>

                                                                    <!--<v-sheet>
                                                                        <v-skeleton-loader :loading="loading" :transition="transition" height="94" type="list-item-two-line">
                                                                            <template>
                                                                                <v-expansion-panels accordion>
                                                                                    <v-expansion-panel v-for="(move, index) in pokemonData.moves">
                                                                                        <v-expansion-panel-header>
                                                                                            <strong>{{move.name| capiReplace}}</strong>
                                                                                        </v-expansion-panel-header>
                                                                                        <v-expansion-panel-content text="left">
                                                                                            {{move.desc}}
                                                                                        </v-expansion-panel-content>
                                                                                    </v-expansion-panel>
                                                                                </v-expansion-panels>
                                                                            </template>
                                                                        </v-skeleton-loader>
                                                                    </v-sheet>-->
                                                                    
                                                                    

                                                                </v-card-text>
                                                            </v-card>
                                                        </v-tab-item>
                                                        <!-- movimientos -->

                                                        <!-- evoluciones -->
                                                        <v-tab-item>
                                                            <v-card flat>
                                                                <v-card-text>
                                                                    <v-sheet>
                                                                        <v-skeleton-loader :loading="loading" :transition="transition" height="94" type="list-item-avatar, list-item-three-line">
                                                                            <v-list class="text-left" subheader>
                                                                                <!--<v-subheader>Evoluciones</v-subheader>-->

                                                                                <v-list-item v-for="(evo, index) in pokemonData.evolutions" >
                                                                                    <v-list-item-avatar rounded="false">
                                                                                        <v-img :src="evo.poke_img"></v-img>
                                                                                    </v-list-item-avatar>

                                                                                    <v-list-item-content>
                                                                                        <v-list-item-title> {{evo.species_name | capitalize }}</v-list-item-title>
                                                                                            <!--{{ evo.desc[0] }}-->
                                                                                            <!--<v-list-item-subtitle> {{ evo.desc[0] }} </v-list-item-subtitle>-->
                                                                                        <v-list-item-content class="text--primary"> {{ evo.desc[0] }} </v-list-item-content>

                                                                                    </v-list-item-content>

                                                                                    <v-list-item-icon>
                                                                                        <v-btn color="light-blue darken-2">
                                                                                            <v-icon small>double_arrow</v-icon>
                                                                                        </v-btn>
                                                                                    </v-list-item-icon>

                                                                                    <!--<v-list-item-icon>
                                                                                        <v-icon :color="chat.active ? 'deep-purple accent-4' : 'grey'">
                                                                                            mdi-message-outline
                                                                                        </v-icon>
                                                                                    </v-list-item-icon>-->
                                                                                </v-list-item>
                                                                            </v-list>
                                                                        </v-skeleton-loader>
                                                                    </v-sheet>

                                                                </v-card-text>
                                                            </v-card>
                                                        </v-tab-item>
                                                        <!-- evoluciones -->

                                                    </v-tabs-items>
                                                    <!-- tabs content -->
                                                    
                                                    <!--<v-card-text>
                                                        <div class="text-h2 pa-12">{{poke.name}}</div>
                                                    </v-card-text>-->
                                                    <v-card-actions class="justify-end">
                                                        <v-btn text  @click="dialog.value = false">Close</v-btn>
                                                    </v-card-actions>
                                                </v-card>
                                            </template>
                                            <!-- Dialog popup -->
                                        </v-dialog>
                                    </v-col>
                                </v-row>

                                <!--<v-spacer></v-spacer>-->
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>
            </v-fade-transition>
        </v-container>
    </div>
</template>

<script>
import axios from 'axios';
import Pokemon from 'pokemon-images';


const API_URL = 'https://pokeapi.co/api/v2/pokemon/';
const API_URL_LIST = 'https://pokeapi.co/api/v2/pokemon/?offset='
const API_ABILITY = 'https://pokeapi.co/api/v2/ability/'
const API_DESC_POKE = 'https://pokeapi.co/api/v2/pokemon-species/'
//const URL_IMG_POKE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/' //7.png'

const URL_IMG_POKE = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/' //7.png'
//https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/1.png

export default ({        
    data() {
        return {
            pokemons:[],
            pokemonData: [],
            pokeAbility:[],
            show: false,
            alignments: [ 'start','center','end'],
            api_init: [0,100],
            tab: 0,
            tabs: ['informacion','habilidades', 'movimientos', 'evoluciones'],
            info: ['stats', 'abilities', 'height', 'moves', 'sprites','weight', 'types','base_experience','id'],
            chip_colors: ['red darken-1', 'pink darken-1','purple darken-1','deep-purple darken-1','green darken-1','amber darken-1','blue-grey darken-1'],
            text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do .',
            inject: {
                theme: {
                    default: { isDark: false },
                },
            },
            loading: true,
            transition: "scale-transition",
        }
    },
    methods:{       
        /* API Calls */
        async getData(){            
            axios.get(API_URL_LIST + this.api_init[0] + '&limit=' + this.api_init[1])
            .then(response => this.pokemons = response.data.results)
            .catch(function (error) {
                // handle error
                console.log(error);
            }).then(function () {
                // always executed
            });
        },
        async getPokeData(name){
            //console.log(this.pokemons)
            this.loading = true
            const { data: poke } = await axios.get(API_URL + name);
            const { data: desc } = await axios.get(API_DESC_POKE + name);

            this.pokemonData = poke
            this.pokemonData.descripcion = desc.flavor_text_entries.find(item => item.language.name === 'es').flavor_text
            this.pokemonData.specie_id = desc.id
            this.pokemonData.evolution_url = desc.evolution_chain.url
            
            /** estadisticas */
            let stat_tmp = []
            for(var a in this.pokemonData.stats){
                let { data: w } = await axios.get(this.pokemonData.stats[a].stat.url);                
                stat_tmp.push({
                    name: w.names.find(item => item.language.name === 'es').name, 
                    value: this.pokemonData.stats[a].base_stat
                })
            }
            this.pokemonData.stats = stat_tmp
            
            /** tipo */
            let type_tmp = []
            for(var a in this.pokemonData.types){
                let { data: w } = await axios.get(this.pokemonData.types[a].type.url);                
                type_tmp.push({
                    name: w.names.find(item => item.language.name === 'es').name
                })
            }
            this.pokemonData.types = type_tmp
            console.log(type_tmp)

            /** habilidades */
            let abis_tmp = []
            for(var a in this.pokemonData.abilities){
                let { data: w } = await axios.get(this.pokemonData.abilities[a].ability.url);
                abis_tmp.push({
                    name: w.names.find(item => item.language.name === 'es').name, 
                    desc: w.flavor_text_entries.find(item => item.language.name === 'es').flavor_text
                })
            }
            this.pokemonData.abilities = abis_tmp
            
            /** movimientos */
            let moves_tmp = []
            for(var a in this.pokemonData.moves){
                let { data: w } = await axios.get(this.pokemonData.moves[a].move.url)
                moves_tmp.push({
                    name: w.names.find(item => item.language.name === 'es').name, 
                    desc: w.flavor_text_entries.find(item => item.language.name === 'es').flavor_text
                })
            }
            this.pokemonData.moves = moves_tmp

            /** evolution */
            let { data: evo }= await axios.get(this.pokemonData.evolution_url)
            this.pokemonData.evolutions = this.evolution(evo)
            
            console.log('aaaaa')
            console.log(this.pokemonData)
            console.log('aaaaa')
            this.loading = false
        },
        evolution(data){
            //https://stackoverflow.com/a/55853073/8872132
            let evoChain = [];
            let evoData = data.chain;
            do {
                let numberOfEvolutions = evoData.evolves_to.length;
                let tmp = this.getDesc(this.getId(evoData.species.url))

                /*console.log(this.getDesc(this.getId(evoData.species.url)))
                console.log(typeof(this.getDesc(this.getId(evoData.species.url))))*/
                //console.log(tmp)

                evoChain.push({
                    "species_name": evoData.species.name,
                    "poke_img": this.getImage(evoData.species.url),
                    "desc": tmp
                });

                if(numberOfEvolutions > 1) {
                    let tmp = this.getDesc(this.getId(evoData.species.url))
                    for (let i = 1;i < numberOfEvolutions; i++) { 
                        evoChain.push({
                            "species_name": evoData.evolves_to[i].species.name,
                            "poke_img": this.getImage(evoData.species.url),
                            "desc": tmp
                        });
                    }
                }
                evoData = evoData.evolves_to[0];
            } while (evoData != undefined && evoData.hasOwnProperty('evolves_to'));
            return evoChain;
        },
        getImage(url){
            return URL_IMG_POKE + this.getId(url) + '.png'
        },
        getDesc(id){
            let tmp = []
            axios.get(API_DESC_POKE + id).then(response => {
                tmp.push(response.data.flavor_text_entries.find(item => item.language.name === 'es').flavor_text);
            })
            return tmp
        },
        getId(url){
            return url.split('/')[url.split('/').length -2]
        },
        /* img pokemon 
        getPokeImg(name){
            return Pokemon.getSprite(name);
        },*/
        searchImg(name){
        },
        random() {
            return Math.floor(Math.random() * this.chip_colors.length).toString()
        },
        height(value){
            //decimetros a centimetros a metros
            return value * 10/100
        },
        weight(value){
            //decagramos a kilogramos
            return value/10
        },
        test(val){
            console.log(val)
        }
    },
    created(){
        this.getData();
        //this.getPokeData('ivysaur');
    },
    filters: {
        capitalize: function (value) {
            if (!value) return ''
            value = value.toString()
            return value.charAt(0).toUpperCase() + value.slice(1)
        },
        capiReplace(value){
            if (!value) return ''
            value = value.toString().replace('-',' ')
            return value.charAt(0).toUpperCase() + value.slice(1)
        }
    }
})
</script>

<style>
.background-img-card{background: #00b09b; /* fallback for old browsers */
	background: -webkit-linear-gradient(to bottom, #00b09b, #96c93d); /* Chrome 10-25, Safari 5.1-6 */
	background: linear-gradient(to bottom, #00b09b, #96c93d);}
</style>

/* eslint-disable */