import React, {Component} from 'react';
import {observable} from 'mobx';
import {inject, observer} from "mobx-react";

import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Stepper from '@material-ui/core/Stepper';
import Step from '@material-ui/core/Step';
import StepLabel from '@material-ui/core/StepLabel';
import CircularProgress from "@material-ui/core/CircularProgress/CircularProgress";
import StepConnector from '@material-ui/core/StepConnector';

import f from "common-ui/utils/f";
import BaseContainer from 'containers/base_container';
import {createFSForm} from 'common-ui/lib/form/fs_form';
import VEvaluationDetailsForm, {evaluation_form_def} from 'components/audits/evaluation/v_evaluation_details_form';
import CEvaluationPurposeForm from "containers/audits/evaluation/c_evaluation_purpose_form";
import CEvaluationCategoriesForm from "containers/audits/evaluation/c_evaluation_categories_form";

@inject("evaluationStore")
@observer
class CEvaluationForm extends Component {
  @observable _vState = {
    application: '',
    saving: false,
    purposeResponse: null,
    categoriesResponse: null,
    categories: [],
    static_prompts: [{"prompt": "", "criteria": ""}]
  }
	constructor(props) {
		super(props);

    this.evalForm = createFSForm(evaluation_form_def);
    this.state = {
      activeStep: 0
    };
	}

  handleRedirect = () => {
    this.props.history.push('/eval_configs');
  }

  handleBackButton = () => {
    this.handleRedirect();
  }

  handlePostCreate = (response) => {
    //handle post final form submission
    this.props.history.replace('/eval_configs/');
  }

  handleCreate = async () => {
    const form = this.evalForm;
    const formData = form.toJSON();
    const data = {
      purpose: formData.purpose,
      name: formData.name,
      categories: formData.categories,
      custom_prompts: [],
      application_ids: formData.application_ids
    };

    try {
      this._vState.saving = true;
      let response = await this.props.evaluationStore.saveEvaluationConfig(data);
      this._vState.saving = false;
      f.notifySuccess('You evaluation is triggered successfully');
      this.handlePostCreate(response);
      this._vState.saving = false;
    } catch(e) {
      this._vState.saving = false;
      f.handleError()(e);
    }
  }

  getSteps = () => {
    return ['Details', 'Purpose', 'Categories'];
  }

  handleNext = async () => {
    const { activeStep } = this.state;
    const form = this.evalForm;
    if (activeStep === 0) {
      if (!form.fields.name.value) {
        f.notifyError("Please fill in the required fields.");
        return;
      }
    } else if (activeStep == 1) {
      if (!form.fields.purpose.value) {
        f.notifyError("Please fill in the required fields.");
        return;
      }
      const data = { purpose: form.fields.purpose.value };
      try {
        this._vState.saving = true;
        let response = await this.props.evaluationStore.addCategories(data);
        this._vState.purposeResponse = response;
        this._vState.saving = false;
      } catch (e) {
        this._vState.saving = false;
        f.handleError()(e);
        return;
      }
    }
    this.setState((prevState) => ({
      activeStep: prevState.activeStep + 1
    }));
  }

  handleBack = () => {
    this.setState((prevState) => ({
      activeStep: prevState.activeStep - 1
    }));
  }

  handleReset = () => {
    this.setState({
      activeStep: 0
    });
  }

  renderStepContent = (step) => {
    switch (step) {
      case 0:
        return <VEvaluationDetailsForm form={this.evalForm} _vState={this._vState}/>;
      case 1:
        return <CEvaluationPurposeForm form={this.evalForm} _vState={this._vState}/>;
      case 2:
        return <CEvaluationCategoriesForm form={this.evalForm} _vState={this._vState}/>;
      default:
        return 'Unknown step';
    }
  }

  handleSaveConfiguration = () => {
    console.log("Save Configuration");
  } 

  render() {
    const {handleBackButton, handleCreate, handleSaveConfiguration} = this;
    const { activeStep } = this.state;
    const steps = this.getSteps();
	return (
		<BaseContainer
      showRefresh={false}
      showBackButton={true}
      backButtonProps={{
      size: 'small',
      onClick: handleBackButton
      }}
      titleColAttr={{
        sm: 8,
        md: 8
      }}
		>
      <Paper>
        <Grid container spacing={1} ref={ref => this.containerRef = ref}>
          <Grid item xs={12} sm={3} className='border-right'>
            <Stepper activeStep={activeStep} orientation="vertical" connector={<StepConnector style={{padding: 0}} />} >
              {steps.map((label, index) => (
              <Step key={label}>
                <StepLabel>{label}</StepLabel>
              </Step>
              ))}
            </Stepper>
          </Grid>
          <Grid item xs={12} sm={9}>
            {this.renderStepContent(activeStep)}
            <Grid container spacing={3} justify="space-between">
              <Grid item></Grid>
              <Grid item xs={12}>
                <Button
                  disabled={activeStep === 0 || this._vState.saving}
                  onClick={this.handleBack}
                  className="m-r-sm"
                >
                  Back
                </Button>
                {activeStep === steps.length - 1 && (
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleSaveConfiguration}
                  data-testid="save-config-btn"
                  data-track-id="save-config-btn"
                  disabled={this._vState.saving}
                  className="m-l-sm"
                >
                  Save Configuration
                </Button>
                )}
                <Button
                  variant="contained"
                  color="primary"
                  onClick={activeStep === steps.length - 1 ? handleCreate : this.handleNext}
                  data-testid="create-app-btn"
                  data-track-id="create-app-btn"
                  disabled={this._vState.saving}
                >
                  {activeStep === steps.length - 1 ? 'Save And Run' : 'Next'}
                  {
                    this._vState.saving &&
                    <CircularProgress size="15px" className="m-r-xs" />
                  }
                </Button>
                {activeStep === steps.length && (
                  <Button onClick={this.handleReset}>
                    Reset
                  </Button>
                )}
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Paper>
	  </BaseContainer>
	)}
}

export default CEvaluationForm;