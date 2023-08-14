document.addEventListener("DOMContentLoaded",function(){
    const inputFahren= document.getElementById("fahrenheit");
    const inputCels= document.getElementById("celsius");
    const inputKelv= document.getElementById("kelvin");
    const convertbtn = document.getElementById("convert");
    const clearbtn = document.getElementById("clear");

    function convertTemps(input){
        const value= parseFloat(input.value);
        if(!isNaN(value)){
            if(input === inputFahren){
                inputCels.value = ((value-32)*5/9).toFixed(3);
                inputKelv.value = ((value-32)*5/9 + 273).toFixed(3);
            }
            else if(input === inputCels){
                inputFahren.value = ((value*9/5)+32).toFixed(3);
                inputKelv.value = (value + 273).toFixed(3);
            }
            else{
                inputFahren.value = (((value-273)*9/5)-32).toFixed(3);
                inputCels.value = (value-273).toFixed(3);
            }
        }
        else{
            if(input === inputFahren){
                inputFahren.value = "Give Number";
            }
            else if(input === inputCels){
                inputCels.value = "Give Number";
            }
            else{
                inputKelv.value = "Give Number";
            }
        }
    }
    convertbtn.addEventListener("click" , function(){
        if(inputFahren.value !== ""){
            convertTemps(inputFahren);
        }
        else if(inputCels.value !== ""){
            convertTemps(inputCels);
        }
        else{
            convertTemps(inputKelv);
        }
    });
    clearbtn.addEventListener("click", function(){
        inputFahren.value="";
        inputCels.value="";
        inputKelv.value="";
    });
});