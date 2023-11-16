<script type="ts">
    import {
        Modal,
        Form,
        FormGroup,
        Select,
        SelectItem,
        Loading,
        Grid,
        Row,
        Column,
        TextInput,
        CodeSnippet, NumberInput, Checkbox
    } from "carbon-components-svelte";
    import Rocket from "carbon-icons-svelte/lib/Rocket.svelte";
    import {v4 as uuid} from 'uuid';
    import {capitalize} from "$lib";

    // props
    export let api;
    export let gyms;
    export let configurations;
    export let run;
    export let runs;

    let loading = false;
    let selectedGym;
    $: selectedGym = gyms?.filter(gym => gym.id === run?.gym_id)[0];
    let params = {};

    let initParamDefaults = () => {
        params = {};
        gyms?.filter(gym => gym.id === run?.gym_id)[0].params.map((param) => {
            params[param.id] = param.type === "bool" ? Number(param.default) ? true : false : param.default;
        });
    };

    $: if (run?.gym_id) {
        initParamDefaults();
    }

    let previewCode = (gym, values) => {
        let code = gym?.code;
        if (gym?.params?.length > 0) {
            for (let param of gym.params) {
                code = code.replaceAll(
                    `%${param.name.toUpperCase().replace(" ", "_")}`,
                    param.type === "bool" ? values[param.id] ? "True" : "False" : values[param.id]
                );
            }
        }
        return code;
    }
</script>

<Loading active={loading}/>

<Modal
        open={run !== null}
        modalHeading="Edit run"
        primaryButtonText="Run"
        primaryButtonIcon={Rocket}
        secondaryButtonText="Cancel"
        selectorPrimaryFocus="#gym-id"
        hasForm
        preventCloseOnClickOutside
        shouldSubmitOnEnter={false}
        size="lg"
        on:click:button--secondary={() => (run = null)}
        on:open
        on:close
        on:submit={()=>{
                run.created_on = new Date();
                loading = true;
                let run_ref = run;
                run_ref["gym_params"] = [];
                for(let param_id of Object.keys(params)) {
                    run_ref.gym_params.push({
                        id: uuid(),
                        run_id: run.id,
                        gym_param_id: param_id,
                        value: params[param_id],
                        created_on: new Date()
                    });
                }
                run = null;
                api.run(run_ref).then(() => {
                    api.getRuns().then(result => {
                        loading = false;
                        runs = result;
                    });
                });
        }}
>
    {#if run}
        <Form on:submit>
            <Grid noGutter fullWidth>
                <Row>
                    <Column>
                        <Grid noGutter fullWidth>
                            <Row>
                                <Column>
                                    <FormGroup>
                                        <Select id="gym-id" labelText="Select gym" bind:selected={run.gym_id}>
                                            {#each gyms as gym}
                                                <SelectItem value={gym.id} text={gym.name}/>
                                            {/each}
                                        </Select>
                                    </FormGroup>
                                </Column>
                            </Row>
                            <Row>
                                <Column>
                                    <FormGroup>
                                        <Select id="configuration-id" labelText="Select configuration"
                                                bind:selected={run.configuration_id}>
                                            {#each configurations as configuration}
                                                <SelectItem value={configuration.id} text={configuration.name}/>
                                            {/each}
                                        </Select>
                                    </FormGroup>
                                </Column>
                            </Row>
                            {#if selectedGym?.params?.length > 0}
                                <Row>
                                    <Column>
                                        <FormGroup legendText="Gym parameters">
                                            <Grid noGutter fullWidth padding>
                                                {#each selectedGym.params as param}
                                                    <Row>
                                                        <Column>
                                                            {#if param["type"] === "str"}
                                                                <TextInput
                                                                        size="sm"
                                                                        bind:value={params[param.id]}
                                                                        labelText={capitalize(param.name)}
                                                                        helperText={param.description}
                                                                        invalidText={param.description}
                                                                        invalid={!params[param.id]}
                                                                        on:keyup={() => {
                                                                            params = params;
                                                                        }}
                                                                />
                                                            {:else if param["type"] === "int"}
                                                                <NumberInput
                                                                        size="sm"
                                                                        bind:value={params[param.id]}
                                                                        labelText={capitalize(param.name)}
                                                                        helperText={param.description}
                                                                        invalidText={param.description}
                                                                        invalid={!params[param.id]}
                                                                        on:keyup={() => {
                                                                            params = params;
                                                                        }}
                                                                />
                                                            {:else if param["type"] === "float"}
                                                                <NumberInput
                                                                        size="sm"
                                                                        bind:value={params[param.id]}
                                                                        labelText={capitalize(param.name)}
                                                                        helperText={param.description}
                                                                        invalidText={param.description}
                                                                        invalid={!params[param.id]}
                                                                        on:keyup={() => {
                                                                            params = params;
                                                                        }}
                                                                        step={0.1}
                                                                />
                                                            {:else if param["type"] === "bool"}
                                                                <Checkbox
                                                                        labelText={capitalize(param.name)}
                                                                        bind:checked={params[param.id]}
                                                                        on:check={() => {
                                                                            params = params;
                                                                        }}
                                                                />
                                                                <span style="font-size: 12px;">{param.description}</span>
                                                            {/if}
                                                        </Column>
                                                    </Row>
                                                {/each}
                                            </Grid>
                                        </FormGroup>
                                    </Column>
                                </Row>
                            {/if}
                        </Grid>
                    </Column>
                    <Column>
                        <CodeSnippet code={previewCode(selectedGym, params)} type="multi" expanded/>
                    </Column>
                </Row>
            </Grid>
        </Form>
    {/if}
</Modal>