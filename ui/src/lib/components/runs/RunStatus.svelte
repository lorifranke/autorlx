<script type="ts">
    import {InlineLoading} from "carbon-components-svelte";
    import {capitalize} from "$lib";

    export let status;
</script>

{#if status === "new" || status === "running"}
    <InlineLoading status="active" description={capitalize(status)}/>
{:else if status === "success" || status === "finished"}
    <InlineLoading status="finished" description={capitalize(status)}/>
{:else if status === "failed" || status === "error"}
    <InlineLoading status="error" description={capitalize(status)}/>
{/if}