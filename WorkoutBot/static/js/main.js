$(document).ready(function () {

    const projectTypeOptions = {
        'Full Body': 'Full Body workouts',
        'Upper Body-Strength': 'Upper body focus strength training',
        'Lower Body-Strength': 'Lower body focus strength training',
        'Weight Loss': 'Focus on weight loss and loosing body fat and strength training incorporated',
        'General': 'General workout plan with a mix of strength training and cardio',
    };

    const buildProjectTypeOptions  = {
        'Full Body Workouts': 'Full Body workouts',
        'Ab Focus': 'Core only ab based workout',
        'Booty Builder': 'Glute Focus',
        'Upper Body': 'Upper Body Focus',
        'Cardio': 'Cardio focused workouts',
        'HIIT Sessions': 'HIIT workout ideas',
        'Stretch': 'Stretch',
        'Pilates':'Pilates style workouts'
        }

    const projectTypeDropdown = $('#project_type_dropdown');
    const buildProjectTypeDropdown = $('#build_project_type_dropdown');

    $.each(projectTypeOptions, function(key, value) {
        projectTypeDropdown.append($('<option>', {
            value: key.toLowerCase(),
            text: key
        }));
    });

    $.each(buildProjectTypeOptions, function(key, value) {
        buildProjectTypeDropdown.append($('<option>', {
            value: key,
            text: key
        }));
    });

    const referencPreferenceDropDown = $("#reference_preference")

    const referencePreferanceOptions= {"Home (none)": "home no equipment","Home (dumbbell)": "dumbbell only","Gym": "gym"}
    
    $.each(referencePreferanceOptions, function(key, value) {
        referencPreferenceDropDown.append($('<option>', {
            value:  value,
            text: key
        }));
    });

    const mealTypeDropDown = $("#mealType")

    const mealTypeOptions= {"Breakfast": "Breakfast","Lunch": "Lunch","Dinner": "Dinner","Snack": "Snack","Sweet Treats":"Sweet Treats"}
    
    $.each(mealTypeOptions, function(key, value) {
        mealTypeDropDown.append($('<option>', {
            value:  value,
            text: key
        }));
    });
    const mealLocDropDown = $("#mealLoc")

    const mealLocOptions= {"Cooking": "Recipes","Something Quick": "Healthy fast food or pre-cooked alternatives"}
    
    $.each(mealLocOptions, function(key, value) {
        mealLocDropDown.append($('<option>', {
            value:  value,
            text: key
        }));
    });


    const experienceDropDown = $("#experience")

    const experienceOptions= {"Beginer": "beginer","Intermediate": "intermediate"}
    

    $.each(experienceOptions, function(key, value) {
        experienceDropDown.append($('<option>', {
            value:  value,
            text: key
        }));
    });

    const timeCommitDropDown = $("#timeCommit")

    const timeCommitOptions= {"15 minutes": "15 minutes","30 minutes": "30 minutes","45 minutes": "45 minutes","60 minutes": "60 minutes","90 minutes":"90 minutes"}
    

    $.each(timeCommitOptions, function(key, value) {
        timeCommitDropDown.append($('<option>', {
            value:  value,
            text: key
        }));
    });

    function createTimeDurationObject() {
        let durations = [];

        for (let i = 1; i <= 20; i++) {
            durations.push({ key: `${i} hour${i > 1 ? 's' : ''}`, value: i });
        }
    
        for (let i = 1; i <= 30; i++) {
            durations.push({ key: `${i} day${i > 1 ? 's' : ''}`, value: i * 24 });
        }
    
        
        for (let i = 1; i <= 9; i++) {
            durations.push({ key: `${i} month${i > 1 ? 's' : ''}`, value: i * 30 * 24 });
        }
    
        
        durations.sort((a, b) => a.value - b.value);
    
        
        const sortedDurations = {};
        durations.forEach(duration => {
            sortedDurations[duration.key] = duration.value;
        });
    
        return sortedDurations;
    }
    
    const timeFrameOptions = createTimeDurationObject()

    const timeFrameDropdown = $("#timeframe")


    

    $.each(timeFrameOptions, function(key, value) {
        timeFrameDropdown.append($('<option>', {
            value: key,
            text: key
        }));
    });

    const timeConstraintsDropdown = $("#time_constraint")


    

    $.each(timeFrameOptions, function(key, value) {
        timeConstraintsDropdown.append($('<option>', {
            value: key,
            text: key
        }));
    });


    const baseUrl = window.location.origin;

    const converter = new showdown.Converter();
    
    /** WORKOUT PLAN SECTION */

    $('#workoutPlanSubmitBtn').on('click', function() {
        (async function() {
            try {
                $('#workoutPlanSubmitBtn').prop('disabled', true);
                $('#spinner').removeClass('hidden');
                const form = document.getElementById('workoutPlanForm');
                const formData = new FormData(form);
                formData.forEach(function(value, key) {
                    if(!value) {
                        throw new Error('Some fields are missing');
                    }
                });
                const response = await fetch(`${baseUrl}/workout_plan_creator`, {
                    method: 'POST',
                    body: formData
                })
                if(!response.ok) {
                    throw new Error('Something went wrong');
                }
                const data = await response.json();
                const html = converter.makeHtml(data.response);
                $('#workoutPlanResponse').html(html);
                $('#workoutPlanResponseContainer').removeClass('hidden');
            } catch (error) {
                console.log(error);
                if(error.message) {
                    $('#workoutPlanErrorMessageContainer').removeClass('hidden').addClass('flex');
                    $('#workoutPlanErrorMessage').text(error.message);
                }
            }
            finally {
                $('#workoutPlanSubmitBtn').prop('disabled', false);
                $('#spinner').addClass('hidden');
            }
        })();
    });

    $('#closeWorkoutPlanErrorBtn').on('click', function() {
        $('#workoutPlanErrorMessageContainer').removeClass('flex').addClass('hidden');
    });

    /** NUTRITION ADVICE SECTION */

    $('#explainConceptSubmitBtn').on('click', function() {
        (async function() {
            try {
                $('#explainConceptSubmitBtn').prop('disabled', true);
                $('#spinner').removeClass('hidden');
                const form = document.getElementById('explainConceptForm');
                const formData = new FormData(form);
                formData.forEach(function(value, key) {
                    if(!value) {
                        throw new Error('Some fields are missing');
                    }
                });
                const response = await fetch(`${baseUrl}/explain_concept`, {
                    method: 'POST',
                    body: formData
                })
                if(!response.ok) {
                    throw new Error('Something went wrong');
                }
                const data = await response.json();
                const html = converter.makeHtml(data.response);
                $('#explainConceptResponse').html(html);
                $('#explainConceptResponseContainer').removeClass('hidden');
            } catch (error) {
                console.log(error);
                if(error.message) {
                    $('#explainConceptErrorMessageContainer').removeClass('hidden').addClass('flex');
                    $('#explainConceptErrorMessage').text(error.message);
                }
            }
            finally {
                $('#explainConceptSubmitBtn').prop('disabled', false);
                $('#spinner').addClass('hidden');
            }
        })();
    });

    $('#closeExplainConceptErrorBtn').on('click', function() {
        $('#explainConceptErrorMessageContainer').removeClass('flex').addClass('hidden');
    });

    /** WORKOUT IDEA SECTION */

    $('#workoutSubmitBtn').on('click', function() {
        (async function() {
            try {
                $('#workoutSubmitBtn').prop('disabled', true);
                $('#spinner').removeClass('hidden');
                const form = document.getElementById('workoutForm');
                const formData = new FormData(form);
                formData.forEach(function(value, key) {
                    if(!value) {
                        throw new Error('Some fields are missing');
                    }
                });
                const response = await fetch(`${baseUrl}/workout`, {
                    method: 'POST',
                    body: formData
                })
                if(!response.ok) {
                    throw new Error('Something went wrong');
                }
                const data = await response.json();
                const html = converter.makeHtml(data.response);
                $('#workoutResponse').html(html);
                $('#workoutResponseContainer').removeClass('hidden');
            } catch (error) {
                console.log(error);
                if(error.message) {
                    $('#workoutErrorMessageContainer').removeClass('hidden').addClass('flex');
                    $('#workoutErrorMessage').text(error.message);
                }
            }
            finally {
                $('#workoutSubmitBtn').prop('disabled', false);
                $('#spinner').addClass('hidden');
            }
        })();
    });

    $('#closeWorkoutErrorBtn').on('click', function() {
        $('#workoutErrorMessageContainer').removeClass('flex').addClass('hidden');
    });

});