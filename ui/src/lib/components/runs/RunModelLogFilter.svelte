<script type="ts">
    import {Form, Grid, Row, Column, FormGroup, MultiSelect, Tile} from "carbon-components-svelte";
    import {unique} from "$lib";

    // props
    export let logs;
    export let filter_phases;
    export let filter_epochs;
    export let filter_iterations;
</script>

<Tile light>
    <h5>Filter</h5>
    <Form class="no-fieldset-bottom">
        <Grid noGutter fullWidth>
            <Row style="margin-top: 20px;">
                <Column>
                    <FormGroup>
                        <MultiSelect
                                placeholder="Phase..."
                                spellcheck="false"
                                items={unique(logs.map(log => log.phase)).map(e => {return {id: e, text: e};})}
                                bind:selectedIds={filter_phases}
                                size="sm"
                                filterable
                        />
                    </FormGroup>
                </Column>
                <Column>
                    <FormGroup>
                        <MultiSelect
                                placeholder="Epoch..."
                                spellcheck="false"
                                items={unique(logs.map(log => log.epoch)).map(e => {return {id: e, text: String(e)};})}
                                bind:selectedIds={filter_epochs}
                                size="sm"
                                filterable
                        />
                    </FormGroup>
                </Column>
                <Column>
                    <FormGroup>
                        <MultiSelect
                                placeholder="Episode..."
                                spellcheck="false"
                                items={unique(logs.map(log => log.iteration)).map(e => {return {id: e, text: String(e)};})}
                                bind:selectedIds={filter_iterations}
                                size="sm"
                                filterable
                        />
                    </FormGroup>
                </Column>
            </Row>
        </Grid>
    </Form>
</Tile>