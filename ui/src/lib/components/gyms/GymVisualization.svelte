<script>
    import * as THREE from "three";
    import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
    import {ProgressBar} from "carbon-components-svelte";

    // props
    export let api;
    export let gym;
    export let visualizationError;
    export let initialize;
    export let timedInit;
    export let width = "100%";
    export let height = "calc(100vh - 252px)";
    export let hideLoading = false;
    export let step;
    export let action;
    export let state;
    export let score = Math.random() * 2 - 1;

    // internal housekeeping
    let container;
    let loaded = false;

    let renderer = new THREE.WebGLRenderer({alpha: true});
    let scene = new THREE.Scene();
    let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    let controls = new OrbitControls(camera, renderer.domElement);

    let init = () => {
        if (!loaded && container && renderer && action && state) {
            renderer.setClearColor(0x000000, 0);
            container.appendChild(renderer.domElement);
            camera.position.z = 5;

            function animate() {
                requestAnimationFrame(animate);
                renderer.render(scene, camera);
            }

            scene.clear();
            try {
                onContainerResize();
                eval(gym?.visualization);
            } catch (e) {
                console.error(e);
            }
            window.addEventListener("resize", onContainerResize);
            animate();
            loaded = true;
        } else {
            onContainerResize();
        }
    };

    let onContainerResize = () => {
        let box = container?.getBoundingClientRect();
        if (box) {
            renderer.setSize(box.width, box.height);
            camera.aspect = box.width / box.height;
            camera.updateProjectionMatrix();
        }
        if (renderer) {
            renderer.render(scene, camera);
        }
    }

    $: if (initialize) {
        init();
    }

    $: if (!step && api) {
        let spaces = structuredClone(gym.spaces);
        if (gym?.params?.length > 0) {
            for (let param of gym.params) {
                spaces.observation.low = spaces.observation.low.replaceAll(`%${param.name.toUpperCase().replace(" ", "_")}`,
                    param.type === "bool" ? param.default ? "True" : "False" : param.default);
                spaces.observation.high = spaces.observation.high.replaceAll(`%${param.name.toUpperCase().replace(" ", "_")}`,
                    param.type === "bool" ? param.default ? "True" : "False" : param.default);
                spaces.action.low = spaces.action.low.replaceAll(`%${param.name.toUpperCase().replace(" ", "_")}`,
                    param.type === "bool" ? param.default ? "True" : "False" : param.default);
                spaces.action.high = spaces.action.high.replaceAll(`%${param.name.toUpperCase().replace(" ", "_")}`,
                    param.type === "bool" ? param.default ? "True" : "False" : param.default);
            }
        }
        api.probeSpace(spaces.observation).then(probe_observation => {
            api.probeSpace(spaces.action).then(probe_action => {
                state = probe_observation.value;
                action = probe_action.value;
                init();
            });
        });
    }

    $: if (step && state && action) {
        scene.clear();
        eval(gym?.visualization);
        onContainerResize();
    }

    if (timedInit) {
        setTimeout(() => {
            initialize = true;
        }, 0);
    }

    // code updates
    $: if (gym?.visualization && state && action) {
        try {
            scene.clear();
            eval(gym?.visualization);
            visualizationError = null;
            onContainerResize();
        } catch (e) {
            visualizationError = e;
        }
    }
</script>

{#if !loaded && !hideLoading}
    <ProgressBar size="sm" helperText="Loading 3D visualization environment..."/>
{/if}
<div bind:this={container}
     style={`min-width:${width}; width:${width}; max-width:${width}; min-height:${height}; height:${height}; max-height:${height};`}></div>
