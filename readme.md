# Dropout prediction API
dropout prediction API from Dropout_and_Success_student_Data_Analysis.csv . API uses flask framework and model used is Randomforest Classification


### Features
- marital_status
- application_mode
- course
- previous_qualification
- tuition_fees_up_to_date
- scholarship_holder
- age_at_enrollment
- curricular_units_1st_sem_credited
- curricular_units_1st_sem_enrolled
- curricular_units_1st_sem_evaluations
- curricular_units_1st_sem_approved
- curricular_units_1st_sem_grade
- inflation_rate

### Labels
- Dropout
- Enrolled
- Graduate


## You can install them using the following command:

```bash
pip install -r requirements.txt
```


### environment example
```bash
//in .env_example

DATABASE_USERNAME=//your database username
DATABASE_PASSWORD=//your database passowrd
DATABASE_NAME=//your database name
```


# API Endpoints
### POST /predict?name={}
- **Description**:Predict the dropout rate
- **Request Body**:
```json
  {
    "marital_status": ,
    "application_mode": ,
    "course": ,
    "previous_qualification": ,
    "tuition_fees_up_to_date": ,
    "scholarship_holder": ,
    "age_at_enrollment": ,
    "curricular_units_1st_sem_credited": ,
    "curricular_units_1st_sem_enrolled": ,
    "curricular_units_1st_sem_evaluations": ,
    "curricular_units_1st_sem_approved": ,
    "curricular_units_1st_sem_grade": ,
    "inflation_rate": 
  } 
```

### GET /history
- **Description**:Get all prediction history
- **Response Body**:
```json
{
  "data" : [
    {
      "features" :  , 
      "id" : ,
      "name" : ,
      "scaled_features" : ,
      "timestamp" : 
    }
  ] ,
  "success" : boolean
}
```

