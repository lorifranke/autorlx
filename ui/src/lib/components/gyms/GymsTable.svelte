<script type="ts">
    import {
        DataTable, CodeSnippet, OverflowMenu, OverflowMenuItem, Toolbar, ToolbarContent, Button, Modal, Form, FormGroup,
        Grid, Row, Column, ComboBox, ToastNotification, Tag, TooltipDefinition, TextInput, InlineNotification
    } from "carbon-components-svelte";
    import Add from "carbon-icons-svelte/lib/Add.svelte";
    import Parameter from "carbon-icons-svelte/lib/Parameter.svelte";
    import View from "carbon-icons-svelte/lib/View.svelte";
    import DecisionTree from "carbon-icons-svelte/lib/DecisionTree.svelte";
    import CatalogPublish from "carbon-icons-svelte/lib/CatalogPublish.svelte";
    import {v4 as uuid} from 'uuid';
    import {cloneGym, capitalize} from "$lib";
    import GymVisualization from "./GymVisualization.svelte";

    // props
    export let api;
    export let gyms;
    export let gym;
    export let runs;
    export let catalog;

    // internal housekeeping
    let catalogGym = null;
    let lastPublishedDate = null;
    let lastUnpublishedDate = null;

    function shouldFilterItem(item, value) {
        if (!value) return true;
        return item.text.toLowerCase().includes(value.toLowerCase());
    }

    let flattenedCatalog = () => {
        let flattened = [];
        let stack = [];
        stack.push(catalog);
        while (stack.length > 0) {
            let element = stack.pop();
            if (element.categories.length > 0) {
                stack.push(...element.categories);
            } else {
                flattened.push(element);
            }
        }
        return flattened;
    }
</script>

<DataTable
        title="Gyms"
        description="Shows gym environments available in the system."
        headers={[
            { key: "name", value: "Gym" },
            { key: "loc", value: "Lines of code"},
            { key: "created_on", value: "Created on"},
            { key: "overflow", empty: true }
        ]}
        rows={gyms}
        expandable
        sortable
>
    <svelte:fragment slot="expanded-row" let:row>
        <Grid noGutter fullWidth>
            <Row style="margin-top: 20px;">
                <Column>
                    <div class="label">Parameters</div>
                    {#each row.params as param}
                        <TooltipDefinition
                                tooltipText={param.description}
                                direction="bottom" align="start"
                        >
                            <Tag icon={Parameter}>{capitalize(param.name)}</Tag>
                        </TooltipDefinition>
                    {/each}
                </Column>
            </Row>
            <Row style="margin-top: 20px;">
                <Column>
                    <div class="label">Module dependencies</div>
                    {#each row.modules as module}
                        <TooltipDefinition
                                tooltipText={"Module dependency"}
                                direction="bottom" align="start"
                        >
                            <Tag type="blue">{module.module}</Tag>
                        </TooltipDefinition>
                    {/each}
                </Column>
            </Row>
            <Row style="margin-top: 20px;">
                <Column>
                    <div class="label">Spaces</div>
                    <TooltipDefinition tooltipText={"Observation space"} direction="bottom" align="start">
                        <Tag icon={View} type="outline">
                            {capitalize(row.spaces.observation.type)}
                            ({row.spaces.observation.size})
                        </Tag>
                    </TooltipDefinition>
                    <TooltipDefinition tooltipText={"Action space"} direction="bottom" align="start">
                        <Tag icon={DecisionTree} type="outline">
                            {capitalize(row.spaces.action.type)}
                            ({row.spaces.action.size})
                        </Tag>
                    </TooltipDefinition>
                </Column>
            </Row>
            <Row style="margin-top: 20px;">
                <Column sm={2}>
                    <div class="label">Implementation</div>
                    <CodeSnippet
                            style="max-width: 100%; margin-bottom: 40px;"
                            type="multi" expanded code={row.code}
                    />
                </Column>
                <Column sm={2}>
                    <div class="label">Visualization</div>
                    <GymVisualization api={api} gym={row} timedInit/>
                </Column>
            </Row>
        </Grid>
    </svelte:fragment>
    <svelte:fragment slot="cell" let:row let:cell>
        {#if cell.key === "overflow"}
            <OverflowMenu flipped>
                <OverflowMenuItem on:click={()=> {
                    gym = cloneGym(row, uuid());
                }} text="Duplicate"/>
                <OverflowMenuItem on:click={()=> {
                    catalogGym = {
                        id: uuid(),
                        gym_id: row.id,
                        category_id: null,
                        email: null,
                        created_on: new Date()
                    };
                }} text="Publish"/>
                <OverflowMenuItem hasDivider danger on:click={()=> {
                    api.deleteCatalogGym(row.id).then(() =>{
                        lastUnpublishedDate = new Date();
                        api.getCatalog().then(result => {
                            catalog = result;
                        });
                    })
                }} text="Unpublish"/>
                <OverflowMenuItem danger on:click={()=> {
                    api.deleteGym(row.id).then(() => {
                        gyms = gyms.filter(gym => gym.id !== row.id);
                        api.getRuns().then(result => {
                            runs = result;
                        });
                    });
                }} text="Delete"/>
            </OverflowMenu>
        {:else if cell.key === "loc"}
            {row.code.split("\n").length}
        {:else if cell.key === "created_on"}
            {new Date(cell.value).toLocaleDateString()} {new Date(cell.value).toLocaleTimeString()}
        {:else}
            {cell.value}
        {/if}
    </svelte:fragment>
    <Toolbar>
        <ToolbarContent>
            <Button icon={Add}
                    on:click={() => {
                        let gym_id = uuid();
                        let p_gamma = {
                            id: uuid(),
                            gym_id: gym_id,
                            name: "gamma",
                            description: "This is the value of the gamma of the MDP.",
                            type: "float",
                            default: 1,
                            created_on: new Date()
                        };
                        let p_horizon = {
                            id: uuid(),
                            gym_id: gym_id,
                            name: "horizon",
                            description: "This is the horizon of the MDP.",
                            type: "int",
                            default: 100,
                            created_on: new Date()
                        };
                        gym = {
                            id: gym_id,
                            name: "",
                            spaces: {
                                observation: {
                                    "type": "box",
                                    "size": 5,
                                    "low": "[0, 0, 0, 0, 0]",
                                    "high": "[1, 1, 1, 1, 1]"
                                },
                                action: {
                                    "type": "discrete",
                                    "size": 1,
                                    "low": "[0]",
                                    "high": "[1]"
                                }
                            },
                            modules: [],
                            reset: "",
                            step: "",
                            custom: "",
                            code: "",
                            visualization: "",
                            params: [p_gamma, p_horizon],
                            created_on: new Date()
                        };
                    }}
            >
                Create new gym
            </Button>
        </ToolbarContent>
    </Toolbar>
</DataTable>

<Modal
        open={catalogGym !== null}
        class="publish_gym_dialog"
        modalHeading={`Publish`}
        primaryButtonText="Publish"
        primaryButtonIcon={CatalogPublish}
        primaryButtonDisabled={!catalogGym || !catalogGym.category_id || !catalogGym.email}
        secondaryButtonText="Cancel"
        hasForm
        size="lg"
        preventCloseOnClickOutside
        shouldSubmitOnEnter={false}
        on:click:button--secondary={() => (catalogGym = null)}
        on:open
        on:close
        on:submit={()=>{
            api.pushCatalogGym(catalogGym).then(() => {
                catalogGym = null;
                lastPublishedDate = new Date();
                api.getCatalog().then(result => {
                    catalog = result;
                });
            });
        }}
>
    {#if catalogGym}
        <Form on:submit>
            <Grid fullWidth noGutter>
                <Row>
                    <Column>
                        <FormGroup>
                            <ComboBox
                                    titleText="Catalog"
                                    selectedId={"default"}
                                    items={[{id: "default", text: catalog.title}]}
                                    disabled
                                    light
                            />
                        </FormGroup>
                    </Column>
                </Row>
                <Row>
                    <Column>
                        <FormGroup>
                            <ComboBox
                                    titleText="Category"
                                    placeholder="Select category..."
                                    bind:selectedId={catalogGym.category_id}
                                    items={
                                        flattenedCatalog().sort((a, b) => a.title.localeCompare(b.title)).map(cat => {
                                            return {id: cat.id, text: cat.title + " (" + cat.code + ")"}
                                        })
                                    }
                                    {shouldFilterItem}
                            />
                        </FormGroup>
                    </Column>
                </Row>
                <Row>
                    <Column>
                        <FormGroup>
                            <TextInput
                                    placeholder="Enter contact e-mail address..."
                                    labelText="Contact E-Mail"
                                    bind:value={catalogGym.email}
                            />
                        </FormGroup>
                    </Column>
                </Row>
                <Row>
                    <Column>
                        <InlineNotification
                                lowContrast
                                kind="warning-alt"
                                style="max-width: 100%;"
                                title="AutoRL X Catalog Publication Agreement"
                                subtitle="Upon publication you understand and agree your implementation will be made publicly available in the AutoRL X Gym Catalog under GPL 3.0 license. You have made sure no intellectual or property rights are violated and you are the sole author of your submission. The AutoRL X team does not guarantee general availability or uptime of the catalog service and withholds the right to remove your submission from the catalog at any time without prior notification."
                                hideCloseButton
                        />
                    </Column>
                </Row>
            </Grid>
        </Form>
    {/if}
</Modal>

{#if lastPublishedDate}
    <ToastNotification
            style="position: fixed; top: 80px; right: 30px;"
            kind="success"
            title="Success"
            subtitle="The gym has been published to the AutoRL X Gym Catalog."
            caption={lastPublishedDate.toLocaleString()}
            timeout={10000}
            on:close={() => {
                lastPublishedDate = null;
            }}
    />
{/if}

{#if lastUnpublishedDate}
    <ToastNotification
            style="position: fixed; top: 80px; right: 30px;"
            kind="success"
            title="Success"
            subtitle="The gym has been unpublished from the AutoRL X Gym Catalog."
            caption={lastUnpublishedDate.toLocaleString()}
            timeout={10000}
            on:close={() => {
                lastUnpublishedDate = null;
            }}
    />
{/if}