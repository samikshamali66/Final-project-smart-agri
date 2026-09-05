function predictYield() {

    let r = parseFloat(document.getElementById("rainfall").value);
    let t = parseFloat(document.getElementById("temperature").value);
    let h = parseFloat(document.getElementById("humidity").value);

    if(isNaN(r) || isNaN(t) || isNaN(h)){
        document.getElementById("result").innerHTML = "⚠ Enter all values";
        return;
    }

    let result = (r*0.4 + t*0.3 + h*0.3);

    if(result > 100){
        document.getElementById("result").innerHTML = "🌾 High Yield: " + result.toFixed(2);
    }
    else if(result > 60){
        document.getElementById("result").innerHTML = "🌱 Medium Yield: " + result.toFixed(2);
    }
    else{
        document.getElementById("result").innerHTML = "🌿 Low Yield: " + result.toFixed(2);
    }
}