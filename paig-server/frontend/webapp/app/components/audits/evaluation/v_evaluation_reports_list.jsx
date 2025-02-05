import React, { Component, Fragment } from 'react';
import {observer, inject} from 'mobx-react';
import { TableCell, Checkbox, Button } from '@material-ui/core';
import DoneIcon from '@material-ui/icons/Done';
import ClearIcon from '@material-ui/icons/Clear';
import GroupIcon from '@material-ui/icons/Group';

import { ActionButtonsWithPermission } from 'common-ui/components/action_buttons';
import Table from 'common-ui/components/table';
import  {STATUS } from 'common-ui/utils/globals';
import {permissionCheckerUtil} from 'common-ui/utils/permission_checker_util';
import UiState from 'data/ui_state';
import {RefreshButton} from 'common-ui/components/action_buttons';

@inject('evaluationStore')
@observer
class VEvaluationReportTable extends Component{
    constructor(props) {
        super(props);
        this.state = {
            expandedRows: []
        };
    }

  getHeaders = () => {
    const {permission, importExportUtil} = this.props;
    
    let headers = ([
      <TableCell key="1">Report Name</TableCell>,
      <TableCell key="2">Configuration Used</TableCell>,
      <TableCell key="3">Applications Evaluated</TableCell>,
      <TableCell key="5">Report Status</TableCell>,
      <TableCell key="6">Score</TableCell>,
      <TableCell key="7">Created</TableCell>,
      <TableCell width="100px" key="9">Actions</TableCell>
    ])

    return headers; 
  }

  formatPercentage = (value) => {
    const formattedValue = value % 1 === 0 ? value.toFixed(0) : value.toFixed(2);
    return `${formattedValue}%`;
  }


  getResultCell = (model) => {
    if (!model.passed || !model.failed) return "--";
  
    // Convert `passed` and `failed` strings into arrays of numbers
    const passedArray = model.passed.split(",").map((value) => parseInt(value.trim(), 10));
    const failedArray = model.failed.split(",").map((value) => parseInt(value.trim(), 10));
  
    // Calculate percentages for corresponding indices
    return passedArray.map((passed, index) => {
      const failed = failedArray[index] || 0; // Default to 0 if no corresponding `failed` value
      const total = passed + failed;
      const percentage = total ? ((passed / total) * 100).toFixed(2) + "%" : "0%";
  
      return (
        <Fragment key={index}>
          <div>
            {percentage} ({passed}/{total})
          </div>
          {index !== passedArray.length - 1 && <hr />}
        </Fragment>
      );
    });
  };

  getApplicationNameCell = (applicationName) => {
    if (!applicationName) return "--";
    const names = applicationName.split(",").map((name, index) => (
      <Fragment key={index}>
        <div>{name.trim()}</div>
        {index !== applicationName.split(",").length - 1 && <hr />}
      </Fragment>
    ));
    return names;
  };

  getRowData = (model) => {
    const {handleDelete, handleReRun, handleEdit, handleView, permission, importExportUtil, handleInvite} = this.props;
    let rows = [
      <TableCell key="1">{model.name}</TableCell>,
      <TableCell key="2">{model.config_name || "--"}</TableCell>,
      <TableCell key="3">{this.getApplicationNameCell(model.application_name) || "--"}</TableCell>,
      //- <TableCell key="4">{model.application_client || "--"}</TableCell>,
      <TableCell key="5">{model.status || "--"}</TableCell>,
      <TableCell key="7">{this.getResultCell(model)}</TableCell>,
      <TableCell key="8">{model.create_time}</TableCell>,
      <TableCell key="9" column="actions">
          <div className="d-flex">
            <ActionButtonsWithPermission
              permission={permission}
              showPreview={model.status == 'COMPLETED'}
              hideDelete={false}
              onDeleteClick={() => handleDelete(model)}
              onPreviewClick={() => handleView(model)}
            />
            <span>
              <RefreshButton
                data-testid="header-refresh-btn"
                data-track-id="refresh-button"
                wrapItem={false}
                pullRight={false}
                onClick={() => handleReRun(model)}
                disabled={model.status !== 'COMPLETED'}
              />
            </span>

          </div>
        </TableCell>
    ]
    return rows;
  }
  handleContextMenuSelection = () => {}

  render() {
    const { data, pageChange, _vState } = this.props;
    console.log('data', data);
    return (
        <Table
            data={data}
            getHeaders={this.getHeaders}
            getRowData={this.getRowData}
            pageChange={pageChange}
        />
    )
}
}

export default VEvaluationReportTable;
