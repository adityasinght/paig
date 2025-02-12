import React, { Component } from "react";
import VEvaluationCategoriesForm from "components/audits/evaluation/v_evaluation_categories_form";

class CEvaluationCategoriesForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showSuggested: true,
      selectedCategories: []
    };
  }

  handleToggle = () => {
    this.setState((prevState) => ({
      showSuggested: !prevState.showSuggested,
    }));
  };

  handleCheckboxChange = (category) => {
    this.setState((prevState) => ({
      selectedCategories: prevState.selectedCategories.includes(category)
        ? prevState.selectedCategories.filter((c) => c !== category)
        : [...prevState.selectedCategories, category]
    }));
  };

  render() {
    const { selectedCategories, showSuggested } = this.state;
    const { _vState } = this.props;
    const evalCategories = _vState.purposeResponse;
    const filteredCategories = showSuggested ? evalCategories.suggested_categories : evalCategories.all_categories;

    return (
      <VEvaluationCategoriesForm
        selectedCategories={selectedCategories}
        showSuggested={showSuggested}
        handleToggle={this.handleToggle}
        handleCheckboxChange={this.handleCheckboxChange}
        filteredCategories={filteredCategories}
        setSearchTerm={this.setSearchTerm}
      />
    );
  }
}

export default CEvaluationCategoriesForm;