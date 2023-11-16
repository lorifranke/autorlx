<script type="ts">
    import {
        CodeSnippet, Breadcrumb, BreadcrumbItem, ContentSwitcher, Switch, Tile, Grid, Row, OverflowMenuItem,
        Column, SelectableTile, InlineNotification, Tag, DataTable, TooltipDefinition, Button, OverflowMenu,
        StructuredList, StructuredListHead, StructuredListRow, StructuredListBody, StructuredListCell, Modal,
        Loading, Pagination, Tabs, Tab, TabContent
    } from "carbon-components-svelte";
    import ConditionPoint from "carbon-icons-svelte/lib/ConditionPoint.svelte";
    import SupportVectorMachine from "carbon-icons-svelte/lib/SupportVectorMachine.svelte";
    import DeploymentPolicy from "carbon-icons-svelte/lib/DeploymentPolicy.svelte";
    import TextIndent from "carbon-icons-svelte/lib/TextIndent.svelte";
    import SettingsView from "carbon-icons-svelte/lib/SettingsView.svelte";
    import ModelAlt from "carbon-icons-svelte/lib/ModelAlt.svelte";
    import Bot from "carbon-icons-svelte/lib/Bot.svelte";
    import ProgressBarRound from "carbon-icons-svelte/lib/ProgressBarRound.svelte";

    // carbon charts
    import '@carbon/charts-svelte/styles.css';
    import {LineChart} from '@carbon/charts-svelte'
    import RunStatus from "./RunStatus.svelte";
    import RunModelLogFilter from "./RunModelLogFilter.svelte";
    import {capitalize, displayUuid, averageLastK, argMax} from "../../utils";
    import GymVisualization from "../gyms/GymVisualization.svelte";

    // props
    export let api;
    export let theme;
    export let gyms;
    export let configurations;
    export let models;
    export let run;
    export let selectedRunId;

    // internal housekeeping
    let contentIndex = 0
    let selectedAgentIds = [];
    let filter_phases = [];
    let filter_epochs = [];
    let filter_iterations = [];
    let selectedEvaluation;
    let trajectory;
    let step = 0;
    let playLoop = null;
    let loading = false;
    let evaluationPageSize = 10;
    let evaluationPage = 1;

    let selectedAgents = [];
    $: if (selectedAgentIds.length > 0) {
        selectedAgents = run.models.filter(r => selectedAgentIds.includes(r.id));
    }

    let filtered_logs;
    $: if (selectedAgentIds.length > 0) {
        filtered_logs = [];
        selectedAgents.map(model => {
            let logs = model.logs.filter(log => {
                if (filter_phases.length > 0) {
                    if (!filter_phases.includes(log.phase)) {
                        return false;
                    }
                }
                if (filter_epochs.length > 0) {
                    if (!filter_epochs.includes(log.epoch)) {
                        return false;
                    }
                }
                if (filter_iterations.length > 0) {
                    if (!filter_iterations.includes(log.iteration)) {
                        return false;
                    }
                }
                return true;
            });
            filtered_logs = filtered_logs.concat(...logs);
        });
        filtered_logs = filtered_logs.sort((a, b) => new Date(a.created_on) - new Date(b.created_on));
    } else {
        filtered_logs = [];
    }

    let performance_data = {};
    $: if (filtered_logs.length > 0) {
        performance_data = filtered_logs?.filter(log => log.reward).sort((a, b) => a.epoch - b.epoch).map(log => {
            return {
                group: displayUuid(log.run_model_id) + ":" + log.phase,
                epoch: Number(log.epoch),
                value: Number(log.reward)
            }
        });
    }

    let hyperparameters;
    $: if (selectedAgentIds.length > 0) {
        hyperparameters = {};
        selectedAgents.map(model => {
            Object.keys(JSON.parse(model.hyperparameters)).map(hyperparameter => {
                if (!(hyperparameter in hyperparameters)) {
                    hyperparameters[hyperparameter] = {};
                }
                hyperparameters[hyperparameter][model.id] = JSON.parse(model.hyperparameters)[hyperparameter];
            });
        });
    } else {
        hyperparameters = {}
    }

    let policies;
    $: if (selectedAgentIds.length > 0) {
        policies = {};
        selectedAgents.map(model => {
            policies[model.id] = model.policy;
        });
    } else {
        policies = {}
    }

    let renderCode = (gym) => {
        let code = gym?.code;
        if (gym?.params?.length > 0) {
            for (let param of gym.params) {
                code = code.replaceAll(`%${param.name.toUpperCase().replace(" ", "_")}`, run.gym_params.filter(p => p.gym_param_id === param.id)[0].value);
            }
        }
        return code;
    }
</script>

<Breadcrumb noTrailingSlash style="margin-bottom: 30px;">
    <BreadcrumbItem href="/" on:click={()=>selectedRunId = null}>Runs</BreadcrumbItem>
    <BreadcrumbItem isCurrentPage>#{displayUuid(run.id)}</BreadcrumbItem>
</Breadcrumb>
<Tile>
    <Grid noGutter fullWidth>
        <Row>
            <Column md={2}>
                <div class="label">Run</div>
                <div class="labeledValue">
                    <Tag icon={ModelAlt} type="blue">{displayUuid(run.id)}</Tag>
                </div>
            </Column>
            <Column>
                <div class="label">Status</div>
                <div class="labeledValue">
                    <RunStatus status={run.status}/>
                </div>
            </Column>
            <Column>
                <div class="label">Selected gym</div>
                <div class="labeledValue">
                    {gyms.filter(gym => gym.id === run.gym_id)[0].name}
                </div>
            </Column>
            <Column>
                <div class="label">Selected configuration</div>
                <div class="labeledValue">
                    {configurations.filter(configuration => configuration.id === run.configuration_id)[0].name}
                </div>
            </Column>
            <Column>
                <div class="label">Created on</div>
                <div class="labeledValue">
                    {new Date(run.created_on).toLocaleDateString()} {new Date(run.created_on).toLocaleTimeString()}
                </div>
            </Column>
        </Row>
    </Grid>
</Tile>
<Grid noGutter fullWidth>
    <Row>
        <Column md={2}>
            <Tile>
                <h4 style="position: relative;">
                    Agent leaderboard
                    <Button
                            size="small" kind="ghost" style="position: absolute; right: 70px; top: -1px;"
                            on:click={()=>{
                                selectedAgentIds = run.models.map(r => r.id);
                            }}
                    >
                        All
                    </Button>
                    <Button
                            size="small" kind="ghost" style="position: absolute; right: 0px; top: -1px;"
                            on:click={()=>{
                                selectedAgentIds = [];
                            }}
                    >
                        None
                    </Button>
                </h4>
                <div role="group" aria-label="selectable tiles" class="agent_leaderboard"
                     style="max-height: calc(100vh - 300px); overflow-y: scroll; margin-top: 10px;">
                    {#each run.models.sort((a, b) => {
                        if (a.status === "running") {
                            return -1;
                        } else if (b.status === "running") {
                            return 1;
                        }
                        let avgA = averageLastK(a.logs.sort((a, b) => a.epoch - b.epoch).map(log => log.reward), 5);
                        let avgB = averageLastK(b.logs.sort((a, b) => a.epoch - b.epoch).map(log => log.reward), 5);
                        return avgB - avgA;
                    }) as model}
                        <SelectableTile
                                light
                                style="margin-bottom: 20px;"
                                selected={selectedAgentIds.includes(model.id)}
                                on:select={() => {
                                    selectedAgentIds.push(model.id);
                                    selectedAgentIds = selectedAgentIds;
                                }}
                                on:deselect={() => {
                                    selectedAgentIds = selectedAgentIds.filter(a => a !== model.id);
                                    selectedAgentIds = selectedAgentIds;
                                }}
                        >
                            <div class="label">
                                {models.filter(m => m.id === model.model_id)[0].name}
                                <TooltipDefinition
                                        direction="bottom"
                                        align="center"
                                        tooltipText={models.filter(m => m.id === model.model_id)[0].description}>
                                    &#9432;
                                </TooltipDefinition>
                            </div>
                            <div>
                                <Grid noGutter fullWith>
                                    <Row>
                                        <Column md={5}>
                                            <RunStatus status={model.status}/>
                                            <Tag type="outline" icon={Bot}>{displayUuid(model.id)}</Tag>
                                            {#if model.logs.length > 0 && model.status === "running"}
                                                <Tag type="gray" icon={ProgressBarRound}>
                                                    {`${capitalize(model.logs[model.logs.length - 1].phase)} ${model.logs[model.logs.length - 1].epoch}:${model.logs[model.logs.length - 1].iteration}`}
                                                </Tag>
                                            {/if}
                                        </Column>
                                        <Column md={3} class="score" noGutter>
                                            <TooltipDefinition
                                                    direction="bottom"
                                                    align="end"
                                                    class="label"
                                                    tooltipText="Displays the average reward computed over the last 5 epochs.">
                                                Reward
                                            </TooltipDefinition>
                                            <div class="labeledValue">{
                                                averageLastK(model.logs.sort((a, b) => a.epoch - b.epoch).map(log => log.reward), 5).toFixed(3)}</div>
                                        </Column>
                                    </Row>
                                </Grid>
                            </div>
                        </SelectableTile>
                    {/each}
                </div>
            </Tile>
        </Column>
        <Column md={6} style="margin-top: 30px;">
            {#if selectedAgentIds.length === 0}
                <Tile>
                    <Tabs type="container">
                        <Tab label="Run logs"/>
                        <Tab label="Gym"/>
                        <svelte:fragment slot="content">
                            <TabContent>
                                <CodeSnippet
                                        style="max-width: 100%;"
                                        type="multi"
                                        expanded
                                        code={run.logs.map(log => `${new Date(log.created_on).toLocaleDateString()} ${new Date(log.created_on).toLocaleTimeString()} - ${log.severity.toUpperCase()}: ${log.log}`).join("\n")}
                                />
                            </TabContent>
                            <TabContent>
                                <CodeSnippet code={renderCode(gyms.filter(gym => gym.id === run.gym_id)[0])}
                                             type="multi" expanded/>
                            </TabContent>
                        </svelte:fragment>
                    </Tabs>
                </Tile>
            {:else}
                <ContentSwitcher
                        size="xl"
                        bind:selectedIndex={contentIndex}
                        style="margin-bottom: 30px;"
                >
                    <Switch>
                        <div style="display: flex; align-items: center;">
                            <ConditionPoint style="margin-right: 0.5rem;"/>
                            Performance
                        </div>
                    </Switch>
                    <Switch>
                        <div style="display: flex; align-items: center;">
                            <TextIndent style="margin-right: 0.5rem;"/>
                            Agent logs
                        </div>
                    </Switch>
                    <Switch>
                        <div style="display: flex; align-items: center;">
                            <SupportVectorMachine style="margin-right: 0.5rem;"/>
                            Evaluation
                        </div>
                    </Switch>
                    <Switch>
                        <div style="display: flex; align-items: center;">
                            <SettingsView style="margin-right: 0.5rem;"/>
                            Hyperparameters
                        </div>
                    </Switch>
                    <!--                    <Switch>-->
                    <!--                        <div style="display: flex; align-items: center;">-->
                    <!--                            <DeploymentPolicy style="margin-right: 0.5rem;"/>-->
                    <!--                            Learned policies-->
                    <!--                        </div>-->
                    <!--                    </Switch>-->
                </ContentSwitcher>
                {#if contentIndex < 3}
                    <RunModelLogFilter
                            logs={[].concat(...selectedAgents.map(model => model.logs))}
                            bind:filter_phases bind:filter_epochs
                            bind:filter_iterations
                    />
                {/if}
                <Tile>
                    {#if contentIndex === 0}
                        <LineChart
                                data={performance_data}
                                options={{
                                    theme: theme,
                                    height: 'calc(100vh - 486px)',
                                    title: 'Reward over epochs',
                                    curve: 'curveMonotoneX',
                                    axes: {
                                        bottom: {title: "Epochs", mapsTo: 'epoch', scaleType: 'linear' },
                                        left: { title: "Reward", mapsTo: 'value', scaleType: 'linear' }
                                    },
                                    points: {
                                        enabled: false
                                    }
                                }}
                        />
                    {:else if contentIndex === 1}
                        <h5>Agent logs</h5>
                        {#if filtered_logs?.length > 0}
                            <CodeSnippet
                                    style="max-width: 100%;"
                                    type="multi"
                                    expanded
                                    code={filtered_logs?.map(log => `${new Date(log.created_on).toLocaleDateString()} ${new Date(log.created_on).toLocaleTimeString()} [${displayUuid(log.run_model_id)} @ ${capitalize(log.phase)} ${log.epoch}:${log.iteration}] ${log.severity.toUpperCase()}: ${log.log}`).join("\n")}
                            />
                        {:else}
                            <InlineNotification
                                    kind="error"
                                    title="Not found:"
                                    subtitle="Logs are not available. This is likely an error."
                                    lowContrast
                                    hideCloseButton
                            />
                        {/if}
                    {:else if contentIndex === 2}
                        <h5>Evaluation</h5>
                        <DataTable style="margin-top: 10px;"
                                   headers={[
                                        { key: "run_model_id", value: "Agent"},
                                        { key: "epoch", value: "Epoch" },
                                        { key: "iteration", value: "Episode" },
                                        { key: "reward", value: "Reward"},
                                        { key: "overflow", empty: true }
                                    ]}
                                   rows={filtered_logs?.filter(log => log.reward)}
                                   size="compact"
                                   pageSize={evaluationPageSize}
                                   page={evaluationPage}
                                   sortable
                        >
                            <svelte:fragment slot="cell" let:row let:cell>
                                {#if cell.key === "overflow"}
                                    <OverflowMenu flipped>
                                        <OverflowMenuItem on:click={()=> {
                                            loading = true;
                                            api.getTrajectory(row.run_model_id, row.epoch, row.iteration).then(result => {
                                                selectedEvaluation = row;
                                                trajectory = JSON.parse(result.score).map((score, i) => {
                                                   return {
                                                       "id": i,
                                                       "action": JSON.parse(result.action)[i],
                                                       "state": JSON.parse(result.state)[i],
                                                       "score": JSON.parse(result.score)[i]
                                                   };
                                                });
                                                step = 0;
                                                loading = false;
                                            });
                                    }} text="Show trajectory"/>
                                    </OverflowMenu>
                                {:else if cell.key === "run_model_id"}
                                    <Tag size="sm" icon={Bot} type="outline">{displayUuid(cell.value)}</Tag>
                                {:else}
                                    {cell.value}
                                {/if}
                            </svelte:fragment>
                        </DataTable>
                        <Pagination
                                totalItems={filtered_logs?.filter(log => log.reward).length}
                                pageSizes={[10, 50, 100]}
                                bind:pageSize={evaluationPageSize}
                                bind:page={evaluationPage}
                        />
                    {:else if contentIndex === 3}
                        <h5>Hyperparameters</h5>
                        {#if hyperparameters}
                            <StructuredList flush condensed style="margin-top: 12px;">
                                <StructuredListHead>
                                    <StructuredListRow head>
                                        <StructuredListCell head></StructuredListCell>
                                        {#each selectedAgents as model}
                                            <StructuredListCell head>
                                                <Tag type="outline" icon={Bot}>{displayUuid(model.id)}</Tag>
                                            </StructuredListCell>
                                        {/each}
                                    </StructuredListRow>
                                </StructuredListHead>
                                <StructuredListBody>
                                    <StructuredListRow>
                                        <StructuredListCell noWrap>Model</StructuredListCell>
                                        {#each selectedAgents as model}
                                            <StructuredListCell>
                                                <CodeSnippet light code={model.model_id}/>
                                            </StructuredListCell>
                                        {/each}
                                    </StructuredListRow>
                                    {#each Object.keys(hyperparameters) as hyperparameter}
                                        {#if ![].includes(hyperparameter.toLowerCase())}
                                            <StructuredListRow>
                                                <StructuredListCell noWrap>
                                                    {capitalize(hyperparameter)}
                                                </StructuredListCell>
                                                {#each selectedAgents as model}
                                                    <StructuredListCell>
                                                        {#if hyperparameters[hyperparameter][model.id]}
                                                            <CodeSnippet light type="multi" wrapText
                                                                         code={JSON.stringify(hyperparameters[hyperparameter][model.id])}/>
                                                        {:else}
                                                            -
                                                        {/if}
                                                        <!--{#if hyperparameters[hyperparameter][model.id]}-->
                                                        <!--    <ul>-->
                                                        <!--        {#each Object.keys(hyperparameters[hyperparameter][model.id]) as key}-->
                                                        <!--            <li>{key}</li>-->
                                                        <!--        {/each}-->
                                                        <!--    </ul>-->
                                                        <!--{/if}-->
                                                    </StructuredListCell>
                                                {/each}
                                            </StructuredListRow>
                                        {/if}
                                    {/each}
                                </StructuredListBody>
                            </StructuredList>
                        {/if}
                    {:else if contentIndex === 4}
                        <h5>Learned policies</h5>
                        <StructuredList flush condensed style="margin-top: 20px;">
                            <StructuredListHead>
                                <StructuredListRow head>
                                    <StructuredListCell head></StructuredListCell>
                                    <StructuredListCell head>Policy</StructuredListCell>
                                </StructuredListRow>
                            </StructuredListHead>
                            <StructuredListBody>
                                {#each selectedAgents as model}
                                    <StructuredListRow>
                                        <StructuredListCell head>
                                            <Tag type="outline" icon={Bot}>{displayUuid(model.id)}</Tag>
                                        </StructuredListCell>
                                        <StructuredListCell noWrap>
                                            <CodeSnippet type="multi" showMoreLess code={policies[model.id]}/>
                                        </StructuredListCell>
                                    </StructuredListRow>
                                {/each}
                            </StructuredListBody>
                        </StructuredList>
                    {/if}
                </Tile>
            {/if}
        </Column>
    </Row>
</Grid>

<Modal
        open={trajectory}
        modalHeading={`Trajectory`}
        shouldSubmitOnEnter={false}
        size="lg"
        on:open
        on:close={() => {
            trajectory = null;
            selectedEvaluation = null;
        }}
        passiveModal
>
    {#if trajectory}
        <Grid>
            <Row>
                <Column>
                    <div class="label">Agent</div>
                    <div class="labeledValue">
                        <Tag type="outline" icon={Bot}>{displayUuid(selectedEvaluation.run_model_id)}</Tag>
                    </div>
                </Column>
                <Column>
                    <div class="label">Reward</div>
                    <div class="labeledValue">
                        {selectedEvaluation.reward}
                    </div>
                </Column>
                <Column>
                    <div class="label">Epoch</div>
                    <div class="labeledValue">
                        {selectedEvaluation.epoch}
                    </div>
                </Column>
                <Column>
                    <div class="label">Episode</div>
                    <div class="labeledValue">
                        {selectedEvaluation.iteration}
                    </div>
                </Column>
                <Column>
                    <div class="label">{capitalize(selectedEvaluation.severity)}</div>
                    <div class="labeledValue">
                        {selectedEvaluation.log}
                    </div>
                </Column>
            </Row>
        </Grid>
        <GymVisualization
                gym={gyms.filter(gym => gym.id === run.gym_id)[0]}
                action={trajectory[step].action}
                state={trajectory[step].state}
                score={trajectory[step].score}
                hideLoading
                timedInit
                step={step}
        />
        <div class="run_action" style="white-space: pre-line">
            {trajectory[step].action.map(a => a.toFixed(2)).join("\n")}
        </div>
        <div class="run_score">
            <Tag type="purple">Step {step + 1}</Tag>
            <br/>
            {trajectory[step].score}
        </div>
        <div style="text-align: center;">
            <Button
                    kind="ghost"
                    on:click={() => {
                        step = 0;
                    }}
                    disabled={playLoop}
            >
                Reset
            </Button>
            <Button
                    kind="ghost"
                    on:click={() => {
                        step -=1;
                    }}
                    disabled={step === 0 || playLoop}
            >
                Step back
            </Button>
            <Button
                    kind="primary"
                    on:click={() => {
                        step +=1;
                    }}
                    disabled={step >= trajectory.length - 1 || playLoop}
            >
                Step forward
            </Button>
            <Button
                    kind="danger--tertiary"
                    on:click={() => {
                        if(step >= trajectory.length - 1) {
                            step = 0;
                        }
                        playLoop = setInterval(() => {
                            if(step < trajectory.length - 1) {
                                step += 1;
                            } else {
                                window.clearInterval(playLoop);
                                playLoop = null;
                            }
                        }, 50)
                    }}
                    disabled={playLoop}
            >
                Play
            </Button>
            <Button
                    kind="danger--ghost"
                    on:click={() => {
                        window.clearInterval(playLoop);
                        playLoop = null;
                    }}
                    disabled={!playLoop}
            >
                Stop
            </Button>
        </div>
    {/if}
</Modal>

<Loading active={loading}/>