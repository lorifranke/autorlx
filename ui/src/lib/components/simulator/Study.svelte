<script>
    import {Tile, ButtonSet, Button, Column, InlineNotification} from "carbon-components-svelte";

    export let deviceActive;
    export let study_step;
    export let reset;
    export let score;
    export let scores;
    export let SIZE;
    export let time;
</script>

<Column style="max-width: 400px!important;">
    <Tile>
        {#if deviceActive}
            <h3>TMS device is <span class="green">active</span>.</h3>
            <InlineNotification
                    lowContrast
                    kind="info"
                    title="Click again to pause treatment."
                    hideCloseButton
            />
        {:else if scores.length === 0}
            <h3>TMS device is <span class="yellow">inactive</span>.</h3>
            <InlineNotification
                    lowContrast
                    kind="warning"
                    title="Click in simulator to start."
                    hideCloseButton
            />
        {:else}
            <h3>TMS device is <span class="yellow">paused</span>.</h3>
            <InlineNotification
                    lowContrast
                    kind="warning"
                    title="Click again to continue treatment."
                    hideCloseButton
            />
        {/if}
    </Tile>
    <Tile>
        <div class="label" style="text-align: right;">
            Time
        </div>
        <div class="user_score" style="margin-bottom: 10px;">
            {Math.floor((new Date().getTime() - time.getTime()) / 1000)} s
        </div>
        <div class="label" style="text-align: right;">
            Score
        </div>
        <div class="user_score purple" style="margin-bottom: 10px;">
            {(score * 100).toFixed(3)} %
        </div>
    </Tile>
    <ButtonSet stacked>
        <Button
                style="max-width: 100%;"
                kind="primary"
                on:click={() => {
                        if(!deviceActive && scores.length > 0) {
                            study_step = study_step + 1;
                        }
                    }}
                disabled={deviceActive || scores.length === 0}
        >
            Close session and submit recording
        </Button>
        <Button
                style="max-width: 100%;"
                kind="danger--ghost"
                on:click={() => {
                    if(!deviceActive && scores.length > 0) {
                        reset();
                    }
                }}
                disabled={deviceActive || scores.length === 0}>
            Discard and restart new session
        </Button>
        <Button
                style="max-width: 100%;"
                kind="ghost"
                on:click={() => {
                    if(!deviceActive) {
                        study_step = study_step - 1;
                        setTimeout(() => {
                            reset();
                        }, 200);
                    }
                }}
                disabled={deviceActive}
        >
            Back to tutorial
        </Button>
    </ButtonSet>
</Column>
<Column>
    <canvas id="canvas" width={SIZE} height={SIZE} style="border:2px solid #ffffff;"/>
</Column>