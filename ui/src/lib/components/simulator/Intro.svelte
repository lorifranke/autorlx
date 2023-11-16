<script>
    import {
        Tile,
        Link,
        Button,
        ButtonSet,
        Column,
        Grid,
        Row,
        StructuredList,
        StructuredListBody, StructuredListRow, StructuredListCell, StructuredListHead
    } from "carbon-components-svelte";
    import coilsPhoto from './coils_photo.png';
    import neuronsPhoto from './neurons_efield.png';
    import tmsTreatmentPhoto from './tms_clinic_application.png';

    export let study_step;
    export let reset;
</script>

<Column md={1}></Column>
<Column md={6}>
    <Tile>
        <h3>TMS 2D-Simulator</h3>
        <Grid fullWidth noGutter style="margin-top: 20px; margin-bottom: 20px;">
            <Row>
                <Column>
                    <Grid noGutter fullWidth>
                        <Row>
                            <Column>
                                <img src={neuronsPhoto} width="100%" alt="Neurons with Field Photo"/>
                            </Column>
                        </Row>
                        <!--                        <Row>-->
                        <!--                            <Column>-->
                        <!--                                <img src={tmsTreatmentPhoto} width="100%" alt="Treatment of patient with TMS device"/>-->
                        <!--                            </Column>-->
                        <!--                        </Row>-->
                        <Row style="margin-top: 30px;">
                            <Column>
                                <p style="text-align: justify">
                                    Transcranial Magnetic Stimulation (TMS) Simulator is an interactive experience that
                                    allows you to simulate the effects of electromagnetic fields generated from brain
                                    stimulation techniques in 2D. In the real world, the TMS device, as seen in the
                                    picture on the right, can stimulate a brain's neural activity and treat mental
                                    diseases.
                                </p>
                            </Column>
                        </Row>
                        <Row style="margin-top: 30px;">
                            <Column>
                                <ButtonSet>
                                    <Button
                                            kind="primary"
                                            on:click={() => {
                                                study_step = study_step + 1;
                                                setTimeout(() => {
                                                    reset();
                                                }, 500);
                                            }}
                                            size="large"
                                            expressive
                                    >
                                        Start tutorial
                                    </Button>
                                </ButtonSet>
                                <StructuredList flush condensed style="margin-top: 20px;">
                                    <StructuredListHead>
                                        <StructuredListRow head>
                                            <StructuredListCell head>Contact</StructuredListCell>
                                            <StructuredListCell head></StructuredListCell>
                                        </StructuredListRow>
                                    </StructuredListHead>
                                    <StructuredListBody>
                                        <StructuredListRow>
                                            <StructuredListCell>
                                                <Link href="mailto:franke@mpsych.org">Loraine Franke</Link>
                                            </StructuredListCell>
                                            <StructuredListCell>
                                                UMass Boston
                                            </StructuredListCell>
                                        </StructuredListRow>
                                        <StructuredListRow>
                                            <StructuredListCell>
                                                Daniel Karl I. Weidele
                                            </StructuredListCell>
                                            <StructuredListCell>
                                                IBM Research
                                            </StructuredListCell>
                                        </StructuredListRow>
                                        <StructuredListRow>
                                            <StructuredListCell>
                                                Lipeng Ning
                                            </StructuredListCell>
                                            <StructuredListCell>
                                                Harvard Medical School
                                            </StructuredListCell>
                                        </StructuredListRow>
                                        <StructuredListRow>
                                            <StructuredListCell>
                                                Daniel Haehn
                                            </StructuredListCell>
                                            <StructuredListCell>
                                                UMass Boston
                                            </StructuredListCell>
                                        </StructuredListRow>
                                    </StructuredListBody>
                                </StructuredList>
                            </Column>
                        </Row>
                    </Grid>
                </Column>
                <Column>
                    <img src={coilsPhoto} width="100%" alt="Coils Photo"/>
                </Column>
            </Row>
        </Grid>
    </Tile>
</Column>
<Column md={1}></Column>