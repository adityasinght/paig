import React from "react";
import { 
  Paper, 
  Switch, 
  FormControlLabel, 
  Checkbox, 
  FormGroup, 
  FormControl, 
  FormLabel,
  Typography,
  Box
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

const VEvaluationCategories = ({
  selectedCategories,
  showSuggested,
  handleToggle,
  handleCheckboxChange,
  filteredCategories
}) => {
  const classes = useStyles();

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
            <Box key={category.Name} className={classes.checkboxItem}>
              <FormControlLabel
                control={
                  <Checkbox
                    color="primary"
                    checked={selectedCategories.includes(category.Name)}
                    onChange={() => handleCheckboxChange(category.Name)}
                  />
                }
                label={
                  <Typography variant="body1" className={classes.categoryName}>
                    {category.Name}
                  </Typography>
                }
              />
            </Box>
          ))}
        </FormGroup>
      </FormControl>  
    </Paper>
  );
};

export default VEvaluationCategories;
