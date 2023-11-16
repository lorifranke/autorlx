<script>
    import {Column, Button, ButtonSet, Tile, InlineNotification, ProgressBar} from "carbon-components-svelte";
    import {LineChart} from "@carbon/charts-svelte";
    import {onMount} from "svelte";

    // props
    export let api;
    export let selectedView;
    export let scores;
    export let theme;
    export let session_id;

    let recorded = false;

    onMount(() => {
        let session = {
            id: session_id,
            scores: scores.map(s => {
                return {
                    time: s.time,
                    score: s.score,
                }
            })
        };
        api.pushUserStudySession(session).then(() => {
            recorded = true;
        });
    });
</script>

<Column sm={1}></Column>
<Column sm={2}>
    <h1>Thank you for participating in this study!</h1>
    {#if !recorded}
        <ProgressBar style="margin-top: 20px; height: 7px;" labelText="Uploading session data..."/>
    {:else}
        <Tile style="margin-top: 20px; margin-bottom: 20px;">
            <p style="margin-bottom: 10px; text-align: left;" class="user_score">
                You scored <span class="green">{scores[scores.length - 1].score.toFixed(3)} %</span> in <span
                    class="gray50">{Math.floor((scores[scores.length - 1].time - scores[0].time) / 1000) }
                seconds</span>.
            </p>
            <InlineNotification
                    style="margin-bottom: 30px;"
                    lowContrast
                    kind="success"
                    title={`Your session data has been recorded (ID #${session_id.toUpperCase()}).`}
                    hideCloseButton
            />
            <LineChart
                    data={scores}
                    options={{
                    title: "Here is your performance over time:",
                theme: theme,
                height: '400px',
                curve: 'curveMonotoneX',
                axes: {
                    bottom: {title: "Time", mapsTo: 'time', scaleType: 'time' },
                    left: { title: "Score (%)", mapsTo: 'score', percentage: true, includeZero: false, domain: [80, 100] }
                },
                points: {
                    enabled: false
                },
                toolbar: {
                    enabled: false
                },
                legend: {
                    enabled: false
                }
            }}
            />
        </Tile>
        <InlineNotification
                style="margin-bottom: 30px;"
                lowContrast
                kind="info"
                title={`Close this tab or window to exit the simulator.`}
                hideCloseButton
        />
        <ButtonSet>
            <Button kind="tertiary" size="xl" on:click={() => {
                selectedView = "runs";
            }} expressive>Start over
            </Button>
        </ButtonSet>
    {/if}
</Column>
<Column sm={1}></Column>