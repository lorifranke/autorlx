<script type="ts">
    import ConfigurationDialog from "./ConfigurationDialog.svelte";
    import ConfigurationsTable from "./ConfigurationsTable.svelte";

    // props
    export let api;
    export let models;
    export let metrics
    export let tuners
    export let configurations;
    export let runs;

    // internal housekeeping
    let configuration = null;

</script>

<ConfigurationsTable api={api} bind:configurations bind:configuration bind:models bind:runs bind:metrics bind:tuners/>
<ConfigurationDialog api={api} bind:configurations bind:configuration bind:models bind:metrics bind:tuners/>



