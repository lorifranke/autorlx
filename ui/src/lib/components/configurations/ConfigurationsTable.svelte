<script type="ts">
    import {
        DataTable,
        Toolbar,
        ToolbarContent,
        Button,
        OverflowMenu,
        OverflowMenuItem,
        Tag, TooltipDefinition, Grid, Row, Column
    } from "carbon-components-svelte";
    import Add from "carbon-icons-svelte/lib/Add.svelte";
    import {v4 as uuid} from 'uuid';

    // props
    export let api;
    export let models;
    export let metrics;
    export let tuners;
    export let configurations;
    export let runs;
    export let configuration;
</script>

<DataTable
        title="Configurations"
        description="Shows system configurations for optimization runs."
        headers={[
            { key: "name", value: "Configuration" },
            { key: "metric_id", value: "Metric" },
            { key: "tuner_id", value: "Tuner" },
            { key: "num_models", value: "Number of selected models" },
            { key: "created_on", value: "Created on"},
            { key: "overflow", empty: true }
        ]}
        rows={configurations}
        expandable
        sortable
>
    <svelte:fragment slot="expanded-row" let:row>
        <Grid>
            <Row style="margin-top: 20px;">
                <Column>
                    <div class="label">Models</div>
                    {#each models.filter(model => row.models.includes(model.id)) as model}
                        <TooltipDefinition tooltipText={model.description} direction="bottom" align="start">
                            <Tag size="sm" type="purple"
                                 style="margin-bottom: 10px; margin-top: 10px;">{model.name}</Tag>
                        </TooltipDefinition>
                        <br/>
                    {/each}
                </Column>
                <Column>
                    <div class="label">Metric</div>
                    <TooltipDefinition
                            direction="bottom"
                            align="center"
                            tooltipText={metrics.filter(m => m.id === row.metric_id)[0].description}>
                        <Tag size="sm" type="teal">{metrics.filter(m => m.id === row.metric_id)[0].name}</Tag>
                    </TooltipDefinition>
                </Column>
                <Column>
                    <div class="label">Tuner</div>
                    <TooltipDefinition
                            direction="bottom"
                            align="start"
                            tooltipText={tuners.filter(t => t.id === row.tuner_id)[0].description}
                    >
                        <Tag size="sm" type="blue">
                            {tuners.filter(t => t.id === row.tuner_id)[0].name}
                        </Tag>
                    </TooltipDefinition>
                </Column>
                <Column>
                    <div class="label">Settings</div>
                    <TooltipDefinition tooltipText={"Number of jobs"} direction="bottom" align="start">
                        <Tag size="sm" style="margin-bottom: 10px; margin-top: 10px;">{row.n_jobs} Jobs</Tag>
                    </TooltipDefinition>
                    <br/>
                    <TooltipDefinition tooltipText={"Number of episodes"} direction="bottom" align="start">
                        <Tag size="sm" style="margin-bottom: 10px; margin-top: 10px;">{row.n_episodes} Episodes</Tag>
                    </TooltipDefinition>
                    <br/>
                    {#if row.metric_id === "genetic"}
                        <TooltipDefinition tooltipText={"Number of agents"} direction="bottom" align="start">
                            <Tag size="sm" style="margin-bottom: 10px; margin-top: 10px;">{row.n_agents} Agents</Tag>
                        </TooltipDefinition>
                        <br/>
                        <TooltipDefinition tooltipText={"Number of generations"} direction="bottom" align="start">
                            <Tag size="sm" style="margin-bottom: 10px; margin-top: 10px;">{row.n_generations}
                                Generations
                            </Tag>
                        </TooltipDefinition>
                        <br/>
                    {/if}
                </Column>
            </Row>
        </Grid>
    </svelte:fragment>
    <svelte:fragment slot="cell" let:row let:cell>
        {#if cell.key === "overflow"}
            <OverflowMenu flipped>
                <OverflowMenuItem on:click={()=> {
                    configuration = {
                        id: uuid(),
                        name: row.name + " (copy)",
                        metric_id: row.metric_id,
                        tuner_id: row.tuner_id,
                        models: row.models.slice(),
                        n_jobs: row.n_jobs,
                        n_episodes: row.n_episodes,
                        n_agents: row.n_agents,
                        n_generations: row.n_generations,
                        created_on: new Date()
                    };
                }} text="Duplicate"/>
                <OverflowMenuItem danger on:click={()=> {
                    api.deleteConfiguration(row.id).then(() => {
                        configurations = configurations.filter(configuration => configuration.id !== row.id);
                        api.getRuns().then(result => {
                            runs = result;
                        });
                    });
                }} text="Delete"/>
            </OverflowMenu>
        {:else if cell.key === "metric_id"}
            {metrics.filter(m => m.id === row.metric_id)[0].name}
        {:else if cell.key === "tuner_id"}
            {tuners.filter(t => t.id === row.tuner_id)[0].name}
        {:else if cell.key === "num_models"}
            {row.models.length}
        {:else if cell.key === "created_on"}
            {new Date(cell.value).toLocaleDateString()} {new Date(cell.value).toLocaleTimeString()}
        {:else}
            {cell.value}
        {/if}
    </svelte:fragment>
    <Toolbar>
        <ToolbarContent>
            <Button icon={Add}
                    on:click={()=>{configuration = {
                        id: uuid(),
                        name: "",
                        metric_id: "discounted",
                        tuner_id: "genetic",
                        models: [],
                        n_jobs: 1,
                        n_episodes: 25,
                        n_agents: 10,
                        n_generations: 50,
                        created_on: new Date()
                    };}}
            >
                Create new configuration
            </Button>
        </ToolbarContent>
    </Toolbar>
</DataTable>