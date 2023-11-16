<script>
    import interpolate from "color-interpolate";
    import {
        Grid, Row
    } from "carbon-components-svelte";
    import Intro from "./Intro.svelte";
    import Tutorial from "./Tutorial.svelte";
    import Study from "./Study.svelte";
    import Finish from "./Finish.svelte";
    import {v4 as uuid} from 'uuid';

    // props
    export let selectedView;
    export let theme;
    export let interpolate_colors = false;
    export let SIZE; // size of brain
    export let N; // number of neurons

    // internal housekeeping
    let study_step = 0;
    let score = 0;
    let scores = [];
    let canvas;
    let ctx;
    let OPT = 100;
    let R = 0.05 * N;   // radius of device
    let n_damages = 50;
    let time = 0;
    let session_id = uuid();
    session_id = session_id.substring(session_id.length - 10, session_id.length);

    // device location
    let device_x = Math.floor(N / 2);
    let device_y = Math.floor(N / 2);

    let grid;
    let square_size = SIZE / N;

    // color map
    let colors = [
        {
            key: OPT * 2,
            value: "#b2182b"
        },
        {
            key: OPT * 1.75,
            value: "#d6604d"
        },
        {
            key: OPT * 1.5,
            value: "#f4a582"
        },
        {
            key: OPT * 1.25,
            value: "#fddbc7"
        },
        {
            key: OPT * 1,
            value: "#ffffff"
        },
        {
            key: OPT * 0.75,
            value: "#e0e0e0"
        },
        {
            key: OPT * 0.5,
            value: "#bababa"
        },
        {
            key: OPT * 0.25,
            value: "#878787"
        },
        {
            key: OPT * 0,
            value: "#4d4d4d"
        }
    ];
    let colormap = interpolate(colors.map(color => color.value));

    function getColorForValue(value) {
        if (interpolate_colors) {
            return colormap(1 - Math.min(value, 200) / 200);
        }
        if (value >= OPT * 2) {
            return colors.filter(c => c.key === 200)[0].value;
        } else if (value >= OPT * 1.75) {
            return colors.filter(c => c.key === 175)[0].value;
        } else if (value >= OPT * 1.5) {
            return colors.filter(c => c.key === 150)[0].value;
        } else if (value >= OPT * 1.25) {
            return colors.filter(c => c.key === 125)[0].value;
        } else if (value >= OPT * 1) {
            return colors.filter(c => c.key === 100)[0].value;
        } else if (value >= OPT * 0.75) {
            return colors.filter(c => c.key === 75)[0].value;
        } else if (value >= OPT * 0.50) {
            return colors.filter(c => c.key === 50)[0].value;
        } else if (value >= OPT * 0.25) {
            return colors.filter(c => c.key === 25)[0].value;
        } else if (value >= 0) {
            return colors.filter(c => c.key === 0)[0].value;
        } else {
            return '#0000ff';
        }
    };

    let renderScene = () => {
        ctx.clearRect(0, 0, SIZE, SIZE);
        // grid
        score = 0;
        for (let x = 0; x < N; x++) {
            for (let y = 0; y < N; y++) {
                ctx.fillStyle = getColorForValue(grid[x][y]);
                ctx.fillRect(Math.floor(x * square_size), Math.floor(y * square_size), Math.ceil(square_size), Math.ceil(square_size));
                score = score + Math.pow(grid[x][y] - OPT, 2)
            }
        }
        score = 1 / ((Math.sqrt(score) / Math.pow(N, 2)) + 1);
        if (deviceActive) {
            scores.push({
                group: session_id,
                time: new Date(),
                score: Number(score * 100)
            });
            scores = scores;
        }
        // draw circle
        if (deviceActive) {
            ctx.fillStyle = 'rgba(208,0,255,0.2)';
        } else {
            ctx.fillStyle = 'rgba(208,0,255,0.2)';
        }
        ctx.beginPath();
        ctx.arc(device_x * square_size, device_y * square_size, R * square_size, 0, 2 * Math.PI);
        ctx.fill();
    };

    let reset = () => {
        scores = [];
        time = new Date();
        // get canvas
        canvas = document.getElementById('canvas');
        canvas.addEventListener('mousemove', onMove);
        canvas.addEventListener("wheel", onWheel);
        canvas.addEventListener("click", onClick);
        ctx = canvas.getContext('2d');
        // init grid
        grid = [];
        for (let x = 0; x < N; x++) {
            grid.push([]);
            for (let y = 0; y < N; y++) {
                grid[x].push(OPT);
            }
        }
        // apply damage
        for (let k = 0; k < n_damages; k++) {
            let kernel_x = Math.floor(Math.random() * N);
            let kernel_y = Math.floor(Math.random() * N);
            for (let x = 0; x < N; x++) {
                for (let y = 0; y < N; y++) {
                    let value = OPT * gauss(kernel_x, kernel_y, x, y, 0.1 * N / 2);
                    grid[x][y] -= value;
                    grid[x][y] = Math.max(0, grid[x][y]);
                }
            }
        }
        renderScene();
    };

    let gauss = (x0, y0, x, y, s) => {
        return Math.exp(-Math.pow(x - x0, 2) / (2 * Math.pow(s, 2)) - Math.pow(y - y0, 2) / (2 * Math.pow(s, 2)));
    }

    let onMove = (e) => {
        device_x = Math.floor(e.offsetX / square_size);
        device_y = Math.floor(e.offsetY / square_size);
        renderScene();
    }

    let onWheel = (e) => {
        e.preventDefault();
        R -= e.deltaY;
        R = Math.min(0.25 * N, Math.max(R, 0.05 * N));
        renderScene();
    }

    let deviceActive;
    let onClick = () => {
        if (deviceActive) {
            clearInterval(deviceActive);
            deviceActive = null;
        } else {
            deviceActive = setInterval(() => {
                for (let x = 0; x < N; x++) {
                    for (let y = 0; y < N; y++) {
                        let value = OPT * gauss(device_x, device_y, x, y, R / 2) / 30;
                        grid[x][y] += value;
                    }
                }
                renderScene();
            }, 50);
        }
    }
    setInterval(() => {
        time = time;
    }, 1000);
</script>

<Grid noGutter fullWidth>
    <Row>
        {#if study_step === 0}
            <Intro
                    bind:study_step
                    reset={reset}
            />
        {:else if study_step === 1}
            <Tutorial
                    bind:study_step
                    deviceActive={deviceActive} theme={theme} colors={colors} reset={reset} scores={scores}
                    score={score} SIZE={SIZE}
            />
        {:else if study_step === 2}
            <Study
                    bind:study_step
                    deviceActive={deviceActive} reset={reset} scores={scores} score={score} SIZE={SIZE} time={time}
            />
        {:else if study_step === 3}
            <Finish
                    bind:selectedView
                    session_id={session_id} scores={scores} theme={theme}
            />
        {/if}
    </Row>
</Grid>