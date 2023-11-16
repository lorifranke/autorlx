<script type="ts">
    import GymDialog from "./GymDialog.svelte";
    import GymsTable from "./GymsTable.svelte";

    // props
    export let api;
    export let gyms;
    export let runs;
    export let catalog;

    // internal housekeeping
    let gym = null;

</script>

<GymsTable api={api} bind:gyms bind:gym bind:runs bind:catalog/>
<GymDialog api={api} bind:gyms bind:gym />

