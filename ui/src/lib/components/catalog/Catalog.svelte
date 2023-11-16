<script>
    import {
        ClickableTile, Tag, Breadcrumb, BreadcrumbItem, ToastNotification, Button, Tile, TooltipDefinition
    } from "carbon-components-svelte";
    import {capitalize} from "$lib";
    import View from "carbon-icons-svelte/lib/View.svelte";
    import ContentView from "carbon-icons-svelte/lib/ContentView.svelte";
    import DecisionTree from "carbon-icons-svelte/lib/DecisionTree.svelte";
    import CalendarHeatMap from "carbon-icons-svelte/lib/CalendarHeatMap.svelte";
    import DotMark from "carbon-icons-svelte/lib/DotMark.svelte";
    import User from "carbon-icons-svelte/lib/UserAvatarFilled.svelte";
    import GymDialog from "../gyms/GymDialog.svelte";
    import {v4 as uuid} from 'uuid';
    import {cloneGym} from "$lib";
    import GymVisualization from "../gyms/GymVisualization.svelte";

    // props
    export let api;
    export let catalog;
    export let gyms;

    // internal housekeeping
    let selections = [];
    let currentCategory;
    let selectedGym = null;
    let lastCopiedDate = null;

    $: if (selections.length > 0) {
        currentCategory = catalog;
        for (let selection of selections) {
            currentCategory = currentCategory.categories.filter(cat => cat.code === selection.code)[0];
        }
    } else {
        currentCategory = catalog;
    }

    let countGyms = (category) => {
        let sum = 0;
        sum += category.gyms?.length;
        for (let subcategory of category.categories) {
            sum += countGyms(subcategory);
        }
        return sum;
    };
</script>
{#if catalog}
    {#if selections.length > 0}
        <h1>NAICS {selections[selections.length - 1].code}</h1>
    {:else}
        <h1>North American Industry Classification System</h1>
    {/if}
    <Breadcrumb noTrailingSlash>
        <BreadcrumbItem
                href="#"
                on:click={()=>{
                selections = [];
            }}
                isCurrentPage={selections.length === 0}
        >
            AutoRL X Catalog
        </BreadcrumbItem>
        {#each selections as selection, i}
            <BreadcrumbItem
                    href="#"
                    on:click={()=>{
                    while(selections[selections.length - 1] !== selection) {
                        selections.pop();
                    }
                    selections = selections;
                }}
                    isCurrentPage={selections.length - 1 === i}
            >
                {selection.title}
            </BreadcrumbItem>
        {/each}
    </Breadcrumb>
    {#each currentCategory.categories as category}
        <ClickableTile
                class={`catalog-tile ${countGyms(category) > 0 ? "has-gyms" : "has-no-gyms"}`}
                on:click={()=>{
                    selections.push(category);
                    selections = selections;
                }}
        >
            <h6>{category.title}</h6>
            <TooltipDefinition
                    tooltipText={"NAICS Code 2022"}
                    direction="bottom"
                    align="start"
            >
                <Tag style="margin-left: 0px;" size="sm">Code {category.code}</Tag>
            </TooltipDefinition>
            <div class="tile-num_gyms">
                {countGyms(category)}
            </div>
        </ClickableTile>
    {/each}
    {#if currentCategory.gyms}
        {#each currentCategory.gyms as catGym, i}
            <Tile class="catalog-tile gym-tile">
                <div style="margin-bottom: 6px; width: 100%; display: inline-block;">
                    <TooltipDefinition
                            tooltipText={"Gym has been published to catalog and is publicly visible to others."}
                            direction="bottom"
                            align="start"
                            style="float: left;"
                    >
                        <Tag style="margin-left: 0px;" type="high-contrast" size="sm">
                            Public gym
                            <svelte:fragment slot="icon">
                                <DotMark class="green"/>
                            </svelte:fragment>
                        </Tag>
                    </TooltipDefinition>
                    <TooltipDefinition
                            tooltipText={"Published on"}
                            direction="bottom"
                            align="start"
                            style="float: left;"
                    >
                        <Tag size="sm" icon={CalendarHeatMap}>
                            {new Date(catGym.created_on).toLocaleDateString()}
                        </Tag>
                    </TooltipDefinition>
                </div>
                <h4>
                    {catGym.name}
                </h4>
                <TooltipDefinition tooltipText={"Contact E-Mail"} direction="bottom" align="start">
                    <Tag icon={User} size="sm">{catGym.email}</Tag>
                </TooltipDefinition>
                <ul style="margin-top: 6px; margin-bottom: 6px;">
                    <li>
                        <div style="width: 30px; float:left; text-align: right;">{catGym.code.split("\n").length}</div>&nbsp;Lines
                        of code
                    </li>
                    <li>
                        <div style="width: 30px; float:left; text-align: right;">{catGym.params.length}</div>&nbsp;Parameters<br/>
                    </li>
                    <li>
                        <div style="width: 30px; float:left; text-align: right;">{catGym.modules.length}</div>&nbsp;Dependencies
                    </li>
                </ul>
                <TooltipDefinition tooltipText={"Observation space"} direction="top" align="start">
                    <Tag icon={View} size="sm" type="outline">
                        {capitalize(catGym.spaces.observation.type)}
                        ({catGym.spaces.observation.size})
                    </Tag>
                </TooltipDefinition>
                <TooltipDefinition tooltipText={"Action space"} direction="top" align="start">
                    <Tag icon={DecisionTree} size="sm" type="outline">
                        {capitalize(catGym.spaces.action.type)}
                        ({catGym.spaces.action.size})
                    </Tag>
                </TooltipDefinition>
                <Button
                        icon={ContentView}
                        size="small"
                        class="clone-from-catalog"
                        on:click={()=>{
                            selectedGym = cloneGym(catGym, uuid());
                        }}
                >
                    View catalog gym
                </Button>
                <div style="position: absolute; bottom: 50px; right: 10px;">
                    <GymVisualization api={api} gym={catGym} timedInit width="150px" height="150px"/>
                </div>
            </Tile>
        {/each}
    {/if}
{/if}

<GymDialog api={api} bind:gyms bind:gym={selectedGym} on:save={() => {lastCopiedDate = new Date();}}/>

{#if lastCopiedDate}
    <ToastNotification
            style="position: fixed; top: 80px; right: 30px;"
            kind="success"
            title="Success"
            subtitle="The gym has been downloaded to your local gyms set."
            caption={lastCopiedDate.toLocaleString()}
            timeout={10000}
            on:close={() => {
                lastCopiedDate = null;
            }}
    />
{/if}
