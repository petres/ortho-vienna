<template>
    <div id="map" ref="mapContainer"/>
    <div v-if="mapLeaflet">
        Zoom: {{ mapLeaflet.getZoom() }}, Bounds: {{ bounds_map }}<br/><br/>
        Combined: <a target="_blank" :href="`/api/img/${img_info()}/PNG`">PNG</a> | <a target="_blank" :href="`/api/img/${img_info()}/JPEG`">JPEG</a><br/><br/>
        <div v-for='m in models'>
            <strong>{{ m }}</strong>: <button @click="addFeatures">Add</button> |
            <a target="_blank" :href="`/api/inf/img-annotated-self/${m}/${img_info()}`">IMG S</a> | 
            <a target="_blank" :href="`/api/inf/img-annotated-yolo/${m}/${img_info()}`">IMG Y</a> | 
            <a target="_blank" :href="`/api/inf/annotation_txt/${m}/${img_info()}`">TXT</a> | 
            <a target="_blank" :href="`/api/inf/annotation_json/${m}/${img_info()}`">JSON</a>
        </div>
        <div v-if="objects">
            {{ objects.length }}
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, shallowRef, markRaw, triggerRef, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router'

import L from "leaflet";
import "leaflet/dist/leaflet.css";

import * as d3 from "d3";
import axios from 'axios';

const router = useRouter()
const route = useRoute()

const props = defineProps({
    layer: String,
    zoom: Number,
    lat: Number,
    lng: Number,
})

const objects = ref(null);
const mapContainer = ref();
const mapLeaflet = shallowRef();
const activeLayer = ref();

import { useStore } from 'vuex'
const store = useStore()

import cap from 'A/data/ortho-cap-vienna.json';

const basemaps = Object.fromEntries(Object.keys(cap).map(lid => {
    const i = cap[lid];
    // console.log({lid, i})
    return [
        lid,
        L.tileLayer(i.url, {
            maxZoom: 20
        })
    ]
}))

const models = computed(() => store.state.models)

const img_info = computed(() => (o) => {
    o ??= {}
    o.zoom ??= mapLeaflet.value.getZoom()
    o.format ??= "JPEG"
    o.layer ??= activeLayer.value
    return `${o.layer}/${bounds_map.value.join('/')}/${o.zoom}`
})

const bounds_map = computed(() => {
    if (!mapLeaflet.value)
        return
    const b = mapLeaflet.value.getBounds()
    // return b
    return [b._southWest.lng, b._southWest.lat, b._northEast.lng, b._northEast.lat]
})

const addFeatures = () => {
    // // axios.get(`/api/inf/annotation_json/${img_info.value()}`).then(d => {
    //     // console.log(d.data)
    //     // const data = d.data
    //     const data = [{
    //         // coordinates: [[[16.366839,48.210032],[16.394906,48.226874]]],
    //         type: "Polygon",
    //         coordinates: [[[16.366839, 48.210032], [16.394906, 48.210032], [16.394906, 48.226874], [16.366839, 48.226874], [16.366839, 48.210032]]],
    //         cls: 1,
    //         conf: 0.88,
    //     }]
        

    //     // data = [16.366839,48.210032,16.394906,48.226874]
    //     objects.value = data
        

            
    //     const areaPaths = g.selectAll('path')
    //         .data(data)
    //         .join('path')
    //         .attr('fill-opacity', 0.3)
    //         .attr('stroke', 'red')
    //         .attr("z-index", 3000)
    //         .attr("fill", "red")
    //         .attr('stroke-width', 2.5)
        
    //     // Function to place svg based on zoom
    //     const onZoom = () => areaPaths.attr('d', pathCreator)
    //     // initialize positioning
    //     onZoom()
    //     // reset whenever map is moved
    //     mapLeaflet.value.on('zoomend', onZoom)
    // // })

}

let g = null;
let pathCreator = null;





onMounted(() => {
    const zoom = props.zoom ? props.zoom : 13;
    const coords = props.lat && props.lng ? [+props.lat, +props.lng] :  [48.2082, 16.3719];
    const layer = props.layer ? props.layer : 'lb';
    var map = L.map(mapContainer.value).setView(coords, zoom);
                // .setBounds()
    // L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //     maxZoom: 19,
    //     attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    // }).addTo(map);

    L.control.layers(basemaps, null, {
        collapsed:false,
    }).addTo(map);
    // var marker = L.marker([51.5, -0.09]).addTo(map);

    mapLeaflet.value = markRaw(map);

    const setRoute = () => {
        const center = map.getCenter();
        router.push({
            name: 'home', params: {
                layer: activeLayer.value,
                lat: center.lat,
                lng: center.lng,
                zoom:  map.getZoom(),
            }
        })
    }

    map.on("moveend", () => {
        setRoute()
        triggerRef(mapLeaflet)
    })
    map.on("zoomend", () => {
        setRoute()
        triggerRef(mapLeaflet)
    })
    map.on("baselayerchange", (e) => {
        setRoute()
        activeLayer.value = e.name
    });

    activeLayer.value = layer
    basemaps[layer].addTo(map);


    // ADDING D3 
    L.svg({clickable:true}).addTo(map) // we have to make the svg layer clickable 
    //Create selection using D3
    const overlay = d3.select(map.getPanes().overlayPane)
    const svg = overlay.select('svg').attr("pointer-events", "auto")
    // create a group that is hidden during zooming
    g = svg.append('g').attr('class', 'leaflet-zoom-hide')

    // Use Leaflets projection API for drawing svg path (creates a stream of projected points)
    const projectPoint = function(x, y) {
        console.log(x,y)
        const point = map.latLngToLayerPoint(new L.LatLng(y, x))
        this.stream.point(point.x, point.y)
    }
    // Use d3's custom geo transform method to implement the above
    const projection = d3.geoTransform({point: projectPoint})
    // creates geopath from projected points (SVG)
    pathCreator = d3.geoPath().projection(projection)
    addFeatures()
});

</script>

<style lang="scss">
#map {
    z-index: 0;
    width: 100%;
    height: 800px;
}
</style>