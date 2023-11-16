<script>
    import {
        Tile,
        Button,
        ButtonSet,
        StructuredList,
        StructuredListHead,
        StructuredListRow,
        StructuredListCell,
        StructuredListBody,
        Column, InlineNotification
    } from "carbon-components-svelte";
    import {LineChart} from "@carbon/charts-svelte";

    export let study_step;
    export let colors;
    export let reset;
    export let SIZE;
    export let theme;
    export let score;
    export let scores;
    export let deviceActive;

    let step = 0;
</script>

<Column style="max-width: 400px!important;">
    {#if step === 0}
        <Tile>
            <h3>Goal</h3>
        </Tile>
        <Tile>
            <p style="text-align: justify">
                The circle on the right represents the electromagnetic field of the TMS device, which you
                can
                manipulate
                using the mouse.
            </p>
            <p style="text-align: justify">
                The background shows an abstraction of a brain region in 2D.
            </p>
            <p style="text-align: justify">
                Each pixel represents a neuron with color signifying varying activity levels.
            </p>
            <h4 style="margin-top: 20px; margin-bottom: 20px;" class="purple">
                <strong>Your goal is to optimize the neurons' activity!</strong>
            </h4>
        </Tile>
    {:else if step === 1}
        <Tile>
            <h3>Controls</h3>
        </Tile>
        <Tile>
            <p style="text-align: justify">
                Move the device with the mouse, change the field strength by scrolling, and click to activate
                the electromagnetic field. Click again to pause the treatment.
            </p>
            <StructuredList condensed flush style="margin-top: 20px;">
                <StructuredListHead>
                    <StructuredListRow head>
                        <StructuredListCell head>In simulator</StructuredListCell>
                        <StructuredListCell head>TMS Device</StructuredListCell>
                    </StructuredListRow>
                </StructuredListHead>
                <StructuredListBody>
                    <StructuredListRow>
                        <StructuredListCell><span style="font-weight: bold">Move mouse</span></StructuredListCell>
                        <StructuredListCell>Moves device</StructuredListCell>
                    </StructuredListRow>
                    <StructuredListRow>
                        <StructuredListCell><span style="font-weight: bold">Scroll</span></StructuredListCell>
                        <StructuredListCell>Change field strength</StructuredListCell>
                    </StructuredListRow>
                    <StructuredListRow>
                        <StructuredListCell><span style="font-weight: bold">Click</span></StructuredListCell>
                        <StructuredListCell>Start treatment</StructuredListCell>
                    </StructuredListRow>
                    <StructuredListRow>
                        <StructuredListCell><span style="font-weight: bold">Click again</span>
                        </StructuredListCell>
                        <StructuredListCell>Pause treatment</StructuredListCell>
                    </StructuredListRow>
                </StructuredListBody>
            </StructuredList>
            <InlineNotification
                    lowContrast
                    kind="info"
                    title="Start practicing in the TMS simulator on the right!"
                    hideCloseButton
            />
        </Tile>
    {:else if step === 2}
        <Tile>
            <h3>Color codes</h3>
        </Tile>
        <Tile>
            <p style="text-align: justify">
                Neural activity is color-coded, with dark grey being inactive, white optimal,
                and red overstimulated. Remember, your goal is to reach an optimal score
                of 100%.
            </p>
            <StructuredList condensed flush style="margin-top: 20px;">
                <StructuredListHead>
                    <StructuredListRow head>
                        <StructuredListCell head>Color</StructuredListCell>
                        <StructuredListCell head>Stimulation level</StructuredListCell>
                    </StructuredListRow>
                </StructuredListHead>
                <StructuredListBody>
                    {#each colors.sort((a, b) => b.value - a.value) as color}
                        <StructuredListRow>
                            <StructuredListCell>
                                <div class="color" style={`background: ${color.value};`}>&nbsp;</div>
                            </StructuredListCell>
                            <StructuredListCell>
                                {color.key} %
                                {#if color.key === 0}
                                    (inactive)
                                {:else if color.key === 100}
                                    (optimal activity)
                                {:else if color.key === 200}
                                    (overly stimulated)
                                {/if}
                            </StructuredListCell>
                        </StructuredListRow>
                    {/each}
                </StructuredListBody>
            </StructuredList>
            <InlineNotification
                    lowContrast
                    kind="warning"
                    title="Avoid to overly stimulate neurons since this cannot be reversed!"
                    hideCloseButton
            />
        </Tile>
    {:else if step === 3}
        <Tile>
            <h3>Score</h3>
        </Tile>
        <Tile>
            <p style="text-align: justify">
                The neurons' aggregate activity is computed as the 'score'.
                During the simulation, the score is continuously recorded over time and displayed in the performance
                chart. Your goal is to reach an optimal overall score of 100%.
            </p>
            <div class="label" style="text-align: right;">
                Score
            </div>
            <div class="user_score purple" style="margin-bottom: 10px;">
                {(score * 100).toFixed(3)} %
            </div>
            <LineChart
                    data={scores}
                    options={{
                        theme: theme,
                        height: '200px',
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
            <InlineNotification
                    lowContrast
                    kind="info"
                    title="Once you are done practicing, close the tutorial and record an actual treatment session!"
                    hideCloseButton
            />
        </Tile>
    {/if}
    <ButtonSet stacked>
        <Button
                style="max-width: 100%;"
                on:click={() => {
                    if(!deviceActive) {
                        if (step < 3 ) {
                            step = step + 1;
                        } else {
                            study_step = study_step + 1;
                            setTimeout(() => {
                                reset();
                            }, 200);
                        }
                    }
                }}
                kind={"primary"}
                disabled={deviceActive}
        >
            {#if step < 3}
                Continue
            {:else}
                Close tutorial and begin session
            {/if}
        </Button>
        {#if step > 0}
            <Button
                    style="max-width: 100%;"
                    kind="secondary"
                    on:click={() => {
                        if(!deviceActive) {
                            reset();
                        }
                    }}
                    disabled={deviceActive}
            >
                Reset simulator
            </Button>
        {/if}
        <Button
                style="max-width: 100%;"
                kind="ghost"
                on:click={() => {
                    if(!deviceActive) {
                        if (step > 0 ) {
                            step = step - 1;
                        } else {
                            study_step = study_step - 1;
                        }
                    }
                }}
                disabled={deviceActive}
        >
            Back
        </Button>
    </ButtonSet>
</Column>
<Column>
    <canvas id="canvas" width={SIZE} height={SIZE} style="border:2px solid #ffffff;"/>
</Column>