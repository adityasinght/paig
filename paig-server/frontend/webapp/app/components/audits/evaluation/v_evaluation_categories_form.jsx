import React from "react";
import { 
  Paper, 
  Switch, 
  FormControlLabel, 
  Checkbox, 
  FormGroup, 
  FormControl,
  Typography,
  Tooltip
} from "@material-ui/core";
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  paper: {
    padding: theme.spacing(3),
  },
  checkboxGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(220px, 1fr))", 
    gap: theme.spacing(2),
  },
  checkboxItem: {
    display: "flex",
    alignItems: "center",
  },
  categoryName: {
    color: theme.palette.text.primary,
  },
}));

const VEvaluationCategories = ({ form, selectedCategories, showSuggested, handleToggle, filteredCategories, setSelectedCategories }) => {
  const { categories } = form.fields;
  const classes = useStyles();

  const handleCheckboxChange = (category) => {
    const updatedCategories = selectedCategories.includes(category)
      ? selectedCategories.filter((c) => c !== category)
      : [...selectedCategories, category];
    setSelectedCategories(updatedCategories);
    console.log(updatedCategories, 'updatedCategories')
    categories.value = updatedCategories;
  };

  return (
    <Paper className={classes.paper}>
      <FormControlLabel
        control={
          <Switch 
            color="primary" 
            checked={showSuggested} 
            onChange={handleToggle} 
          />
        }
        label={<Typography variant="subtitle1">Suggested filters</Typography>}
      />

      <FormControl component="fieldset" fullWidth>
        <Typography variant="h6" className="m-t-sm m-b-sm">
          {showSuggested ? "Suggested Categories" : "All Categories"}
        </Typography>

        <FormGroup className={classes.checkboxGrid}>
          {filteredCategories.map((category) => (
            <FormControlLabel
              key={category.Name}
              control={
                <Checkbox
                  color="primary"
                  checked={selectedCategories.includes(category.Name)}
                  onChange={() => handleCheckboxChange(category.Name)}
                />
              }
              label={
                <Tooltip key={category.Name} title={category.Description} arrow placement="top">  
                  <Typography variant="body1" className={classes.categoryName}>
                    {category.Name}
                  </Typography>
                </Tooltip>
              }
            />
          ))}
        </FormGroup>
      </FormControl>  
    </Paper>
  );
};

export default VEvaluationCategories;
