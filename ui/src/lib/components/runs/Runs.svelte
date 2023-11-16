<script type="ts">
    import Run from "./Run.svelte";
    import RunDialog from "./RunDialog.svelte";
    import RunsTable from "./RunsTable.svelte";

    // props
    export let api;
    export let theme;
    export let gyms;
    export let models;
    export let configurations;
    export let runs;
    export let runsLoaded

    // internal housekeeping
    let run = null;
    let selectedRunId;

    let selectedRun;
    $: if(selectedRunId) {
        selectedRun = runs.filter(r => r.id === selectedRunId)[0];
    }
</script>

{#if selectedRunId && runs}
    <Run
            api={api}
            bind:selectedRunId
            run={selectedRun}
            gyms={gyms}
            models={models}
            configurations={configurations}
            theme={theme}
    />
{:else}
    <RunsTable
            api={api}
            bind:selectedRunId
            bind:run
            gyms={gyms}
            configurations={configurations}
            runs={runs}
            models={models}
            runsLoaded={runsLoaded}
    />
    <RunDialog
            api={api}
            bind:run
            bind:runs
            gyms={gyms}
            configurations={configurations}
    />
{/if}