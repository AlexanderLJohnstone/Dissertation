/*
 * This function takes the radio button that has been checked and converts to a integer
 * The value is then sent using eel to python backend
 */
function callPython() {
    if(document.getElementById('er').checked){
        eel.get_network(1);
        window.location.href = "NetworkParameters.html"
    }
    if(document.getElementById('ws').checked){
        eel.get_network(2);
        window.location.href = "NetworkParameters.html"
    }
    if(document.getElementById('ba').checked){
        eel.get_network(3);
        window.location.href = "NetworkParameters.html"
    }
    if(document.getElementById('rpn').checked){
        eel.get_network(4);
        window.location.href = "NetworkParameters.html"
    }
}

/*
 * This function looks at input fields and checks for valid input
 * This function uses values sent from backend to frontend to dictate validation checks
 * If all is fine the values are sent to backend
 */
function checkInput(){
    var inputs = document.getElementsByTagName("input");
    var i;
    var flag = true;
    var values = [inputs.length];
    for(i = 0; i < inputs.length; i++){
        if (inputs[i].value == "") { // Missing Values
            alert("Error: Please fill all parameters");
            flag = false;
            break;
        }
        if(inputs[i].value < 0){ // Negative values
            alert("Error: Positive values only!");
            flag = false;
            break;
        }
        if(typings[i] === "int"){ // Float in an int space
            if(!Number.isInteger(+inputs[i].value)){
                alert("Error: Not an int!");
                flag = false;
                break;
            }
        }
        if(typings[i] === "float"){ // Received an unexpected value
            if(inputs[i].value > 1){
                alert("Error: Floats must be between 0 and 1!");
                flag = false;
                break;
            }
        }
        values[i] = inputs[i].value;
    }
    if(flag){
        window.location.href = "Loading.html"
        eel.set_values(values)
    }
}

// Typings is a variable to store the values sent between function calls
let typings;

/* This function is called by backend to send the parameters required for the selected graph
 * The function then dynamically converts this information into input fields
 * The function also stores expected data types for other functions
 */
function parameterAdder(text, types) {
    typings = types
    let div = document.getElementById('entry');
    var i;
    for (i = 0; i < text.length;i ++){
        var input = document.createElement("input");
        input.type = "number";
        input.id = text[i];
        input.required = true;
        var label = document.createElement("label")
        label.htmlFor = text[i]
        label.innerHTML = text[i] + " (" + types[i] + ")"
        div.appendChild(label);
        div.innerHTML += "<br>"
        div.appendChild(input);
        div.innerHTML += "<br>"
    }
} eel.expose(parameterAdder);

/*
 * Function that controls display of policies based on checkboxes
 * On click reveal/hide elements of the page
 */
function show_inputs(x) {
    if (document.getElementById(x).checked) {
        let input = document.getElementById(x + "-Entry");
        let label = document.getElementById(x + "-Label");
        let incInput = document.getElementById(x + '-Increment')
        let incLabel = document.getElementById(x + '-Label-Increment')
        // Add Default values
        if(x === "R"){
            input.value = 0.7;
            incInput.value = 0.05
        } else if (x === "Case"){
            input.value = 0.01
            incInput.value = 0.01
        } else if(x == "Variance"){ // If clicked then uncheck other obedience case
           if(document.getElementById("Cluster").checked){
               document.getElementById("Cluster").click()
           }
            input.value = 0.7
            incInput.value = 0.1
        }else if(x == "Cluster"){// If clicked then uncheck other obedience case
            if(document.getElementById("Variance").checked){
               document.getElementById("Variance").click()
           }
            input.value = 0.7
            incInput.value = 0.1
        }
        else if(x == "Tracing"){
            input.value = 0.5
            incInput.value = 0.1
        }
        else if(x == "Isolation"){
            input.value = 0.5
            incInput.value = 0.1
        }
        input.style.display = "inline";
        label.style.display = "inline";
        incInput.style.display = "inline";
        incLabel.style.display = "inline";
        document.getElementById(x).checked = true;
    } else { // If un-clicked hide boxes
        if(x == "Isolation"){
            if(document.getElementById("Tracing").checked){
               document.getElementById("Tracing").click()
           }
        }
        document.getElementById(x + "-Entry").style.display = "none";
        document.getElementById(x + "-Label").style.display = "none";
        document.getElementById(x + '-Increment').style.display = "none";
        document.getElementById(x + '-Label-Increment').style.display = "none";
        document.getElementById(x).checked = false;
    }
}

/*
 * Function to check the sanity of iterator input
 */
function checkIterator(){
    var inputs = document.getElementsByTagName("input");
    var flag = true;
    var values = [inputs.length];
    for(i = 0; i < inputs.length; i++) {
        if (inputs[i].value == "") {
            alert("Error: Please fill all parameters");
            flag = false;
            break;
        }
        if(inputs[i].value < 1){
            alert("Error: Positive integers only!");
            flag = false;
            break;
        }
        if(inputs[0].value < 5){
             alert("Error: At least 5 iterations!");
            flag = false;
            break;
        }
        if(!Number.isInteger(+inputs[i].value)){
            alert("Error: Not an int!");
            flag = false;
            break;
        }
        values[i] = inputs[i].value;
    }
    if(flag){
        window.location.href = "SimulationLoading.html";
        eel.set_sim_values(values[0],values[1]);
    }
}

/*
 * Complex function to check sanity of policy input and prepare it for backend
 * Creates a set of parallel lists to send to back end for model specification
 */
function processInput(){
    let policies = []
    let values = []
    let increments = []
    let R = document.getElementById('R');
    let Case = document.getElementById('Case');
    let variance = document.getElementById('Variance');
    let cluster = document.getElementById('Cluster');
    let isolation = document.getElementById("Isolation")
    let tracing = document.getElementById("Tracing")
    let holders = ["R", "Case", "Variance", "Cluster", "Isolation", "Tracing"]
    let flag = true;
    for(let i = 0; i < holders.length; i++){ // Check sanity and append to lists for each policy
         if (document.getElementById(holders[i]).checked == true) {
             policies.push(holders[i])
             let val = document.getElementById(holders[i] + '-Entry');
             flag = checkVal(val);
             values.push(val.value)
             let inc = document.getElementById(holders[i] + '-Increment');
             if (flag) {
                 flag = checkVal(inc);
                 increments.push(inc.value)
             }
             if(!flag){
                 continue;
             }
         }
    }
    // Obedience must be selected with an intervention policy
    if((!R.checked && !Case.checked) && (variance.checked || cluster.checked)){
        flag = false
        alert("Choose an intervention")
    }
    if(tracing.checked && !isolation.checked){
        flag = false
        alert("Isolation must be in place for contact tracing")
    }
    if(policies.length == 0){
        flag = false
        alert("Select at least one policy")
    }

    if(flag == true){
        eel.set_policy(policies, values, increments)
        window.location.href = "SimulationValues.html"
    }
}

/*
 * Simple sanity check for inputs
 */
function checkVal(element){
    if (element.value < 0 || element.value > 1 || element.value == "") {
        alert('Intervention values Between 1 and 0 only');
        return false
    }
    return true;
}