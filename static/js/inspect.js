function imagePrediction() {
    
    var fileObj = $("#new_file")
    console.log(fileObj);
    
    d3.json('/predict').then(foodData => {
        console.log(foodData);

        //add result to panel
        var PANEL = d3.select("#results");
        PANEL.html("")
        Object.entries(foodData).forEach(([key, value]) => {
            PANEL.append("h6").text(`${key}: ${value}`);
        });
        // var trace1 = {
        //     y: ageData.age_hd,
        //     type: 'box',
        //     name: 'Age w/ HD'
        //   };
    
        //   var trace2 = {
        //     y: ageData.age_no_hd,
        //     type: 'box',
        //     name: 'Age w/o HD'
        //   };
          
        //   var data = [trace1, trace2];
          
        //   Plotly.newPlot('boxplot', data);
    });
}
