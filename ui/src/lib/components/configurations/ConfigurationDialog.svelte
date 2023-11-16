<script type="ts">
    import {
        Modal,
        Form,
        FormGroup,
        TextInput,
        SelectableTile,
        Slider,
        Grid,
        Row, Select, SelectItem,
        Column
    } from "carbon-components-svelte";
    import Save from "carbon-icons-svelte/lib/Save.svelte";

    // props
    export let api;
    export let configurations;
    export let models;
    export let metrics;
    export let tuners;
    export let configuration;
</script>

<Modal
        open={configuration !== null}
        modalHeading="Edit configuration"
        primaryButtonText="Save configuration"
        primaryButtonIcon={Save}
        primaryButtonDisabled={configuration?.name?.length === 0 || configuration?.models?.length === 0}
        secondaryButtonText="Cancel"
        selectorPrimaryFocus="#config-name"
        hasForm
        preventCloseOnClickOutside
        shouldSubmitOnEnter={false}
        on:click:button--secondary={() => (configuration = null)}
        on:open
        on:close
        on:submit={()=>{
            configuration.created_on = new Date();
            api.pushConfiguration(configuration).then(() => {
                configurations.push(configuration);
                configuration = null;
                configurations = configurations;
            });
        }}
>
    {#if configuration}
        <Form on:submit>
            <FormGroup>
                <Grid fullWidth noGutter>
                    <Row>
                        <Column>
                            <TextInput
                                    id="config-name"
                                    labelText="Configuration name"
                                    placeholder="Enter configuration name..."
                                    bind:value={configuration.name}
                            />
                        </Column>
                        <Column>
                            <Select
                                    labelText="Evaluation metric"
                                    bind:selected={configuration.metric_id}
                            >
                                {#each metrics as metric}
                                    <SelectItem value={metric.id} text={metric.name}/>
                                {/each}
                            </Select>
                        </Column>
                        <Column>
                            <Select
                                    labelText="Tuner"
                                    bind:selected={configuration.tuner_id}
                            >
                                {#each tuners as tuner}
                                    <SelectItem value={tuner.id} text={tuner.name}/>
                                {/each}
                            </Select>
                        </Column>
                    </Row>
                    <Row style="margin-top: 20px;">
                        <Column>
                            <Slider labelText="Number of jobs" bind:value={configuration.n_jobs} min={1} max={64}
                                    step={1} fullWidth/>
                        </Column>
                        <Column>
                            <Slider labelText="Number of episodes" bind:value={configuration.n_episodes} min={1}
                                    max={100}
                                    step={1} fullWidth/>
                        </Column>
                    </Row>
                    <Row>
                        <Column>
                            <Slider labelText="Number of agents" bind:value={configuration.n_agents} min={1}
                                    max={100}
                                    step={1}
                                    fullWidth
                                    disabled={configuration.tuner_id !== "genetic"}
                            />
                        </Column>
                        <Column>
                            <Slider labelText="Number of generations" bind:value={configuration.n_generations}
                                    min={1}
                                    max={100}
                                    step={1}
                                    fullWidth
                                    disabled={configuration.tuner_id !== "genetic"}
                            />
                        </Column>
                    </Row>
                </Grid>

            </FormGroup>
            <FormGroup legendText="Select models">
                <div role="group" aria-label="selectable tiles">
                    {#each models as model}
                        <SelectableTile
                                selected={configuration.models.includes(model.id)}
                                on:select={() => {
                                    configuration.models.push(model.id);
                                    configuration = configuration;
                                }}
                                on:deselect={() => {
                                    configuration.models = configuration.models.filter(m => m !== model.id);
                                    configuration = configuration;
                                }}
                                style="margin: 10px; max-width: calc(33% - 20px); float: left; height: 210px; overflow: scroll;"
                                light
                        >
                            {model.name}
                            <div class="bx--form__helper-text">{model.description}</div>
                        </SelectableTile>
                    {/each}
                </div>
            </FormGroup>
        </Form>
    {/if}
</Modal>