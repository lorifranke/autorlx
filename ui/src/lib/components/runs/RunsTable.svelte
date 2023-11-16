<script type="ts">
    import {
        DataTable,
        DataTableSkeleton,
        Toolbar,
        ToolbarContent,
        Button,
        Link,
        OverflowMenu,
        OverflowMenuItem,
        Tag,
        StructuredList,
        StructuredListHead,
        StructuredListBody,
        StructuredListRow,
        StructuredListCell,
        ProgressBar
    } from "carbon-components-svelte";
    import Add from "carbon-icons-svelte/lib/Add.svelte";
    import Bot from "carbon-icons-svelte/lib/Bot.svelte";
    import ProgressBarRound from "carbon-icons-svelte/lib/ProgressBarRound.svelte";
    import ModelAlt from "carbon-icons-svelte/lib/ModelAlt.svelte";
    import {v4 as uuid} from 'uuid';
    import RunStatus from "./RunStatus.svelte";
    import {displayUuid, capitalize, averageLastK} from "../../utils";

    // props
    export let api;
    export let runs;
    export let models;
    export let selectedRunId
    export let configurations;
    export let gyms;
    export let run;
    export let runsLoaded;
</script>

{#if runsLoaded}
    <DataTable
            title="Runs"
            description="Shows runs launched in the system."
            headers={[
                { key: "id", value: "Run" },
                { key: "created_on", value: "Created on" },
                { key: "models", value: "Number of models"},
                { key: "status", value: "Status" },
                { key: "gym_id", value: "Gym"},
                { key: "configuration_id", value: "Configuration"},
                { key: "overflow", empty: true }
            ]}
            rows={runs}
            sortable
            expandable
    >
        <svelte:fragment slot="expanded-row" let:row>
            <StructuredList condensed style="margin-top: 20px; margin-bottom: 0px;">
                <StructuredListHead>
                    <StructuredListRow head>
                        <StructuredListCell head>Agent</StructuredListCell>
                        <StructuredListCell head>Model</StructuredListCell>
                        <StructuredListCell head>Reward</StructuredListCell>
                        <StructuredListCell head>Status</StructuredListCell>
                        <StructuredListCell head>Runtime</StructuredListCell>
                        <StructuredListCell head>Created on</StructuredListCell>
                    </StructuredListRow>
                </StructuredListHead>
                <StructuredListBody>
                    {#each row.models.sort((a, b) => {
                        let avgA = averageLastK(a.logs.sort((a, b) => a.epoch - b.epoch).map(log => log.reward), 5);
                        let avgB = averageLastK(b.logs.sort((a, b) => a.epoch - b.epoch).map(log => log.reward), 5);
                        return avgB - avgA;
                    }) as model}
                        <StructuredListRow>
                            <StructuredListCell>
                                <Tag icon={Bot} type="outline">{displayUuid(model.id)}</Tag>
                            </StructuredListCell>
                            <StructuredListCell>
                                {models?.filter(m => m.id === model.model_id)[0].name}
                            </StructuredListCell>
                            <StructuredListCell>
                                {averageLastK(model.logs.sort((a, b) => a.epoch - b.epoch).map(log => log.reward), 5).toFixed(3)}
                            </StructuredListCell>
                            <StructuredListCell>
                                <RunStatus status={model.status}/>
                                {#if model.logs.length > 0 && model.status === "running"}
                                    <Tag type="gray" icon={ProgressBarRound}>
                                        {`${capitalize(model.logs[model.logs.length - 1].phase)} ${model.logs[model.logs.length - 1].epoch}:${model.logs[model.logs.length - 1].iteration}`}
                                    </Tag>
                                {/if}
                            </StructuredListCell>
                            <StructuredListCell>
                                {
                                    Math.floor((new Date(model.logs[model.logs.length - 1].created_on) - new Date(model.logs[0].created_on)) / 1000 / 60 / 60)
                                } h
                                {
                                    Math.floor(((new Date(model.logs[model.logs.length - 1].created_on) - new Date(model.logs[0].created_on)) / 1000 / 60) % 60)
                                } min
                            </StructuredListCell>
                            <StructuredListCell>
                                {new Date(model.created_on).toLocaleDateString()} {new Date(model.created_on).toLocaleTimeString()}
                            </StructuredListCell>
                        </StructuredListRow>
                    {/each}
                </StructuredListBody>
            </StructuredList>
            <Button size="xl" on:click={()=>{selectedRunId = row.id}}>Open this run
            </Button>
        </svelte:fragment>
        <svelte:fragment slot="cell" let:row let:cell>
            {#if cell.key === "overflow"}
                <OverflowMenu flipped>
                    <OverflowMenuItem danger on:click={()=> {
                    api.deleteRun(row.id).then(() => {
                        runs = runs.filter(run => run.id !== row.id);
                    });
                }} text="Delete"/>
                </OverflowMenu>
            {:else if cell.key === "id"}
                <Link href="#"
                      on:click={()=>{selectedRunId = cell.value}}>
                    <Button kind="ghost" icon={ModelAlt}>{displayUuid(cell.value)}</Button>
                </Link>
            {:else if cell.key === "models"}
                {cell.value.length}
            {:else if cell.key === "status"}
                <RunStatus status={cell.value}/>
            {:else if cell.key === "gym_id"}
                {gyms.filter(gym => gym.id === cell.value)[0].name}
            {:else if cell.key === "configuration_id"}
                {configurations.filter(configuration => configuration.id === cell.value)[0].name}
            {:else if cell.key === "created_on"}
                {new Date(cell.value).toLocaleDateString()} {new Date(cell.value).toLocaleTimeString()}
            {:else}
                {cell.value}
            {/if}
        </svelte:fragment>
        <Toolbar>
            <ToolbarContent>
                <Button icon={Add}
                        disabled={gyms.length === 0 || configurations.length === 0}
                        on:click={()=>{run = {id: uuid(), gym_id: null, configuration_id: null, status: "running"};}}>
                    Create new run
                </Button>
            </ToolbarContent>
        </Toolbar>
    </DataTable>
{:else}
    <ProgressBar style="height: 7px;"/>
    <DataTableSkeleton
            headers={[
                { value: "Run" },
                { value: "Created on" },
                { value: "Status" },
                { value: "Gym" },
                { value: "Configuration" },
                { empty: true },
            ]}
            rows={5}
    />
{/if}